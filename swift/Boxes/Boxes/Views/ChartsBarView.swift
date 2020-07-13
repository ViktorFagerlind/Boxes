//
//  BarChart.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-10.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Charts
import SwiftUI

struct ChartsBarView : UIViewRepresentable
{
  //Bar chart accepts data as array of BarChartDataEntry objects
  var entries : [BarChartDataEntry] = []
  var color: NSUIColor = NSUIColor.red
  var label: String = ""
  var dateAxis = false

  let dateAxisFormatter: DateAxisFormatter = DateAxisFormatter()
  
  init(entries : [BarChartDataEntry], color: NSUIColor = NSUIColor(red:0.8, green: 0.2, blue: 0.3, alpha: 0.8), label: String = "Swims")
  {
    self.entries = entries
    self.color = color
    self.label = label
  }
  
  init(values: [Double], color: NSUIColor = NSUIColor(red:0.8, green: 0.2, blue: 0.3, alpha: 0.8), label: String = "Swims")
  {
    for (i,value) in values.enumerated()
    {
      self.entries.append(BarChartDataEntry(x: Double(i), y: value))
    }

    self.color = color
    self.label = label
  }
  
  init(dates: [String], values: [Double], color: NSUIColor = NSUIColor(red:0.8, green: 0.2, blue: 0.3, alpha: 0.8), label: String = "Swims")
  {
    for (dateString, value) in zip(dates, values)
    {
      self.entries.append(
        BarChartDataEntry(x: stringToDate(dateString: dateString).timeIntervalSince1970,
                          y: value))

    }

    self.color = color
    self.label = label
    dateAxis = true
  }
  
  // this func is required to conform to UIViewRepresentable protocol
  func makeUIView(context: Context) -> BarChartView
  {
    //crate new chart
    let chart = BarChartView()
    //it is convenient to form chart data in a separate func
    
    if dateAxis
    {
      chart.xAxis.valueFormatter = dateAxisFormatter
    }

    chart.data = addData()
    
    return chart
  }

  // this func is required to conform to UIViewRepresentable protocol
  func updateUIView(_ uiView: BarChartView, context: Context)
  {
    //when data changes chartd.data update is required
    uiView.data = addData()
  }

  func addData() -> BarChartData
  {
    let data = BarChartData()
    //BarChartDataSet is an object that contains information about your data, styling and more
    let dataSet = BarChartDataSet(entries: entries)
    // change bars color to green
    dataSet.colors = [color]
    //change data label
    dataSet.label = label
    data.addDataSet(dataSet)
    
    return data
  }

  typealias UIViewType = BarChartView    
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


struct Bar_Previews: PreviewProvider
{
  static var dates: [Date] =
    [stringToDate(dateString: "2019-01-14"),
     stringToDate(dateString: "2019-01-15"),
     stringToDate(dateString: "2019-01-16"),
     stringToDate(dateString: "2019-01-17"),
     stringToDate(dateString: "2019-01-18")]
  
  static var previews: some View
  {
    /*ChartsBarView(entries:
        [
        //x - position of a bar, y - height of a bar
        BarChartDataEntry(x: dates[0].timeIntervalSince1970, y: 2),
        BarChartDataEntry(x: dates[1].timeIntervalSince1970, y: 1),
        BarChartDataEntry(x: dates[2].timeIntervalSince1970, y: 8),
        BarChartDataEntry(x: dates[3].timeIntervalSince1970, y: 2),
        BarChartDataEntry(x: dates[4].timeIntervalSince1970, y: 5)
        ])*/
    
    //ChartsBarView(values: [10.0, 4.0, 6.0, 87.0, 4.0, 65.0, 65.0, 30.0, 10.0])
    
    ChartsBarView(entries:
        [
        //x - position of a bar, y - height of a bar
        BarChartDataEntry(x: 0, y: 10),
        BarChartDataEntry(x: 1, y: 4),
        BarChartDataEntry(x: 2, y: 6),
        BarChartDataEntry(x: 3, y: 87),
        BarChartDataEntry(x: 4, y: 4)
        ])

  }
}
