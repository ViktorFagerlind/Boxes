//
//  LineChart.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-10.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Charts
import SwiftUI

struct ChartsLineView : UIViewRepresentable
{
  //Line chart accepts data as array of LineChartDataEntry objects
  var entries : [ChartDataEntry] = []
  var color: NSUIColor = NSUIColor.red
  var label: String = ""
  var dateAxis = true

  let dateAxisFormatter: DateAxisFormatter = DateAxisFormatter()
  
  init(entries : [ChartDataEntry], color: NSUIColor = NSUIColor(red:0.8, green: 0.2, blue: 0.3, alpha: 0.8), label: String = "Swims")
  {
    self.entries = entries
    self.color = color
    self.label = label
  }
  
  init(values: [Double], color: NSUIColor = NSUIColor(red:0.8, green: 0.2, blue: 0.3, alpha: 0.8), label: String = "Swims")
  {
    for (i,value) in values.enumerated()
    {
      self.entries.append(ChartDataEntry(x: Double(i), y: value))
    }

    self.color = color
    self.label = label
  }
  
  init(dates: [String], values: [Double], color: NSUIColor = NSUIColor(red:0.8, green: 0.2, blue: 0.3, alpha: 0.8), label: String = "Swims")
  {
    for (dateString, value) in zip(dates, values)
    {
      self.entries.append(
        ChartDataEntry(x: stringToDate(dateString: dateString).timeIntervalSince1970,
                       y: value))

    }

    self.color = color
    self.label = label
    dateAxis = true
  }
  
  // this func is required to conform to UIViewRepresentable protocol
  func makeUIView(context: Context) -> LineChartView
  {
    //crate new chart
    let chart = LineChartView()
    //it is convenient to form chart data in a separate func
    
    if dateAxis
    {
      chart.xAxis.valueFormatter = dateAxisFormatter
    }

    chart.data = addData()
    
    return chart
  }

  // this func is required to conform to UIViewRepresentable protocol
  func updateUIView(_ uiView: LineChartView, context: Context)
  {
    //when data changes chartd.data update is required
    uiView.data = addData()
  }

  func addData() -> LineChartData
  {
    let data = LineChartData()
    //LineChartDataSet is an object that contains information about your data, styling and more
    let dataSet = LineChartDataSet(entries: entries)
    dataSet.colors = [color]
    dataSet.circleHoleColor = NSUIColor.black
    dataSet.setCircleColor (color)
    dataSet.label = label
    dataSet.mode = LineChartDataSet.Mode.horizontalBezier
    dataSet.circleRadius = 5.0
    dataSet.circleHoleRadius = 2.5
    dataSet.drawFilledEnabled = true
    dataSet.fillColor = color
    dataSet.lineWidth = 2.0

    data.addDataSet(dataSet)
    
    return data
  }

  typealias UIViewType = LineChartView
}


struct Line_Previews: PreviewProvider
{
  static var dates: [Date] =
    [stringToDate(dateString: "2019-01-14"),
     stringToDate(dateString: "2019-02-15"),
     stringToDate(dateString: "2020-01-16"),
     stringToDate(dateString: "2020-04-17"),
     stringToDate(dateString: "2020-06-18")]
  
  static var previews: some View
  {
    ChartsLineView(entries:
        [
        ChartDataEntry(x: dates[0].timeIntervalSince1970, y: 2),
        ChartDataEntry(x: dates[1].timeIntervalSince1970, y: 1),
        ChartDataEntry(x: dates[2].timeIntervalSince1970, y: 8),
        ChartDataEntry(x: dates[3].timeIntervalSince1970, y: 2),
        ChartDataEntry(x: dates[4].timeIntervalSince1970, y: 5)
        ])
  }
}
