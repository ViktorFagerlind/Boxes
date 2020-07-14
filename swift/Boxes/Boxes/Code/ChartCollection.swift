//
//  PlotInfo.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-09.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Foundation
import Charts
import Yaml

class ChartCollection
{
  static let singleton = ChartCollection()
  
  var charts: [Chart] = []
  
  private init()
  {
    let path = Bundle.main.path(forResource: "tables_and_charts", ofType: "yaml")
    let fm = FileManager()
    let content = fm.contents(atPath: path!)
    let yaml = try! Yaml.load(String(data: content!, encoding: String.Encoding.utf8)!)

    for chartYaml in yaml["charts"].array!
    {
      var plots: [Plot] = []
      for plotYaml in chartYaml["plots"].array!
      {
        // TODO: Assign color
        let plot = Plot(table: plotYaml["table"].string!,
                        kind: plotYaml["kind"].string!,
                        xColumn: plotYaml["x-column"].string!,
                        yColumn: plotYaml["y-column"].string!,
                        color: NSUIColor(red:     CGFloat.random(in: 0.2...1.0),
                                         green:   CGFloat.random(in: 0.2...1.0),
                                         blue:    CGFloat.random(in: 0.2...1.0),
                                         alpha:   0.8))
        plots.append(plot)
      }

      let chart: Chart = Chart(name: chartYaml["name"].string!,
                               category: chartYaml["category"].string!,
                               plots: plots)
      
      charts.append(chart)
    }
  }
}

struct Chart: Hashable
{
  let name: String
  let category: String

  let plots: [Plot]
  
}

struct Plot: Hashable
{
  let table:   String
  let kind:    String
  let xColumn: String
  let yColumn: String
  let color:   NSUIColor

  func getXvalues() -> [String] // TODO: Support other than dates/string
  {
    return TableCollection.singleton.getTable(name: table)!.getColumnData(columnName: xColumn)
  }
  
  func getYValues() -> [Double]
  {
    return TableCollection.singleton.getTable(name: table)!.getColumnData(columnName: yColumn)
  }
}
