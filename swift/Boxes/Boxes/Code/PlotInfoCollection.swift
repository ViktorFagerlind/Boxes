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
                                    kind: "line",
                                    category: yamlPlot["category"].string!,
                                    query: yamlPlot["query"].string!,
                                    columnTypes: [],
                                    columnNames: [],
                                    y_col: 0)
      
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
      
      for (i, col) in yamlPlot["columns"].array!.enumerated()
      {
        if col["name"].string != yamlPlot["x-axis"].string
        {
          plot.y_col = i
          break
        }
      }

      // TODO: There can be many plots...
      plot.kind = yamlPlot["plots"].array![0]["kind"].string!
      
      plots.append(plot)
    }
  }
}

struct PlotInfo: Hashable
{
  var name: String
  var kind: String
  var category: String
  var query: String
  var columnTypes: [Boxes_ColumnType]
  var columnNames: [String]
  var y_col: Int
}
