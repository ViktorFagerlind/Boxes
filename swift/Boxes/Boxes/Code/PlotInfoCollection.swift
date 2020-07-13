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

func findColumnsIndex(array: [Yaml], str: String) -> Int?
{
  for (i,e) in array.enumerated()
  {
    if e["name"].string == str
    {
      return i
    }
  }
  return nil
}

class PlotInfoCollection
{
  let yaml: Yaml
  static let singleton = PlotInfoCollection()
  
  var plots: [PlotInfo] = []
  
  private init()
  {
    let path = Bundle.main.path(forResource: "plots", ofType: "yaml")
    let fm = FileManager()
    let content = fm.contents(atPath: path!)
    yaml = try! Yaml.load(String(data: content!, encoding: String.Encoding.utf8)!)

    for (_, yamlPlot) in yaml.dictionary!
    {
      var plot: PlotInfo = PlotInfo(name: yamlPlot["name"].string!,
                                    category: yamlPlot["category"].string!,
                                    query: yamlPlot["query"].string!)
      
      for col in yamlPlot["columns"].array!
      {
        var type: Boxes_ColumnType = Boxes_ColumnType.unused
        switch col["type"].string!
        {
          case "REAL":      type = Boxes_ColumnType.real
          case "DATETIME":  type = Boxes_ColumnType.datetime
          case "INTEGER":   type = Boxes_ColumnType.integer
          default:          type = Boxes_ColumnType.text
        }
        
        plot.columnNames.append(col["name"].string!)
        plot.columnTypes.append(type)
      }

      plot.x_col = findColumnsIndex(array: yamlPlot["columns"].array!, str: yamlPlot["x-axis"].string!)!
      
      for plt in yamlPlot["plots"].array!
      {
        // TODO: Assign color
        let set = SetInfo(kind: plt["kind"].string!,
                          y_col: findColumnsIndex(array: yamlPlot["columns"].array!, str: plt["y-axis"].string!)!,
                          color: NSUIColor(red:     CGFloat.random(in: 0.2...1.0),
                                           green:   CGFloat.random(in: 0.2...1.0),
                                           blue:    CGFloat.random(in: 0.2...1.0),
                                           alpha:   0.8))
        plot.sets.append(set)
      }

      plots.append(plot)
    }
  }
}

struct PlotInfo: Hashable
{
  var name: String
  var category: String
  var query: String
  var columnTypes: [Boxes_ColumnType] = []
  var columnNames: [String] = []
  var x_col: Int = 0
  var sets: [SetInfo] = []
}

struct SetInfo: Hashable
{
  var kind: String
  var y_col: Int
  var color: NSUIColor
}
