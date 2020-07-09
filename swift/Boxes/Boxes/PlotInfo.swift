//
//  PlotInfo.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-09.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Foundation
import Yaml

class PlotInfoCollection
{
  let yaml: Yaml
  static let singleton = PlotInfoCollection()
  
  var plots: [Plot] = []
  
  private init()
  {
    let path = Bundle.main.path(forResource: "plots", ofType: "yaml")
    let fm = FileManager()
    let content = fm.contents(atPath: path!)
    yaml = try! Yaml.load(String(data: content!, encoding: String.Encoding.utf8)!)

    for (name, plotInfo) in yaml.dictionary!
    {
      var plot: Plot = Plot(name: name.string!,
                            query: plotInfo["query"].string!,
                            columnTypes: [],
                            columnNames: [],
                            y_col: 0)
      
      for col in plotInfo["columns"].array!
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
      
      for (i, col) in plotInfo["columns"].array!.enumerated()
      {
        if col["name"].string != plotInfo["x-axis"].string
        {
          plot.y_col = i
          break
        }
      }
      
      plots.append(plot)
    }
  }
}

struct Plot: Hashable
{
  var name: String
  var query: String
  var columnTypes: [Boxes_ColumnType]
  var columnNames: [String]
  var y_col: Int
}
