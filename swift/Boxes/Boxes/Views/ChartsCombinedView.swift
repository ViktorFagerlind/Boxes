//
//  CombinedChart.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-10.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Charts
import SwiftUI



struct ChartsCombinedView : UIViewRepresentable
{
  //Combined chart accepts data as array of CombinedChartDataEntry objects
  let data = CombinedChartData()

  let dateAxisFormatter: DateAxisFormatter = DateAxisFormatter()
  
  init(chart: Chart)
  {
    initData(chart: chart)
  }
  
  func initData(chart: Chart)
  {
    data.lineData = getLineData(chart: chart)
    data.barData = getBarData(chart: chart)
  }

  func getLineData(chart: Chart) -> LineChartData?
  {
    if !chart.plots.contains(where: {$0.kind == "line"})
    {
      return nil
    }
    
    let lineData: LineChartData = LineChartData()
    
    for plot in chart.plots.filter({$0.kind == "line"})
    {
      let dataSet = LineChartDataSet(entries: createEntries(dates: plot.getXvalues(),
                                                            values: plot.getYValues()))
      
      dataSet.colors = [plot.color]
      dataSet.circleHoleColor = NSUIColor.black
      dataSet.setCircleColor (plot.color)
      dataSet.label = plot.name
      dataSet.mode = LineChartDataSet.Mode.horizontalBezier
      dataSet.circleRadius = 5.0
      dataSet.circleHoleRadius = 2.5
      dataSet.drawFilledEnabled = plot.filled
      dataSet.fillColor = plot.color
      dataSet.lineWidth = 2.0
      //dataSet.drawCirclesEnabled = false
      
      lineData.addDataSet(dataSet)
    }
    
    return lineData
  }

  func getBarData(chart: Chart) -> BarChartData?
  {
    if !chart.plots.contains(where: {$0.kind == "bar"})
    {
      return nil
    }
    
    let barData: BarChartData = BarChartData()
    
    for plot in chart.plots.filter({$0.kind == "bar"})
    {
      let entries = createBarEntries(dates: plot.getXvalues(), values: plot.getYValues())
      let dataSet = BarChartDataSet(entries: entries)
      dataSet.colors = [plot.color]
      dataSet.label = plot.name
      
      barData.addDataSet(dataSet)
      
      let xValues: [Double] = entries.map {$0.x}
      barData.barWidth = calcBarWidth(xRange: barData.xMax-barData.xMin, xValues: xValues)
    }
    
    return barData
  }
  
  // this func is required to conform to UIViewRepresentable protocol
  func makeUIView(context: Context) -> CombinedChartView
  {
    let chart = CombinedChartView()
    chart.xAxis.valueFormatter = dateAxisFormatter
    chart.data = data
    
    return chart
  }

  // this func is required to conform to UIViewRepresentable protocol
  func updateUIView(_ uiView: CombinedChartView, context: Context)
  {
    uiView.data = data
  }

  typealias UIViewType = CombinedChartView
}


struct Combined_Previews: PreviewProvider
{
  static var previews: some View
  {
    ChartsCombinedView(chart: ChartCollection.singleton.charts[0])
  }
}


public class DateAxisFormatter: NSObject, IAxisValueFormatter
{
  private let dateFormatter = DateFormatter()

  override init()
  {
    super.init()
    dateFormatter.dateFormat = "yyyy-MM"
  }

  public func stringForValue(_ value: Double, axis: AxisBase?) -> String
  {
    return dateFormatter.string(from: Date(timeIntervalSince1970: value))
  }
}

func calcBarWidth(xRange: Double, xValues: [Double]) -> Double
{
  var width: Double
  let fillGrade: Double = 0.8
  let minWidth: Double = 0.01

  var minDistance: Double = xRange
  
  for i in 1..<xValues.count
  {
    minDistance = min(minDistance, xValues[i] - xValues[i-1])
  }
  
  if minDistance / xRange < minWidth
  {
    width = minWidth * xRange
  }
  else
  {
    width = minDistance * fillGrade
  }
    
  return width
}

func stringToDate(dateString: String) -> Date
{
  var returnDate: Date?
  let formatter = DateFormatter()
  formatter.dateFormat = "yyyy-MM-dd"
  returnDate = formatter.date(from: dateString)
  
  if returnDate == nil
  {
    formatter.dateFormat = "yyyy-MM"
    returnDate = formatter.date(from: dateString)
  }
  return returnDate!
}


func createEntries(dates: [String], values: [Double]) -> [ChartDataEntry]
{
  var entries: [ChartDataEntry] = []
  
  for (dateString, value) in zip(dates, values)
  {
    entries.append(ChartDataEntry(x: stringToDate(dateString: dateString).timeIntervalSince1970,y: value))
  }
  
  entries.sort(by: { $0.x < $1.x }) // Bug in charts forcing ordering by x
  
  return entries
}

func createBarEntries(dates: [String], values: [Double]) -> [BarChartDataEntry]
{
  var entries: [BarChartDataEntry] = []
  
  for (dateString, value) in zip(dates, values)
  {
    entries.append(BarChartDataEntry(x: stringToDate(dateString: dateString).timeIntervalSince1970,y: value))
  }
  
  return entries
}

