//
//  QueryModels.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-07.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Foundation

class QueryModel: ObservableObject
{
  let plotInfo: PlotInfo
  var loaded: Bool = false

  @Published private(set) var rows: [TableDataRow] = []
  @Published private(set) var y_vals: [Double] = []

  var table: Boxes_Table = Boxes_Table()
  
  init(plotInfo: PlotInfo)
  {
    self.plotInfo = plotInfo
  }
  
  func loadFromDataEngine()
  {
    if loaded {return}
    loaded = true
    
    print("Loading: \(plotInfo.query)")

    table = DataEngineProxy.singleton.executeQuery(query: plotInfo.query, columnTypes: plotInfo.columnTypes)
    y_vals = table.columns[plotInfo.y_col].numValues
    
    updateRows()
  }
  
  private func updateRows ()
  {
    rows.removeAll()
    
    for iv in 0..<table.columns[0].strValues.count
    {
      var line: [String] = []
      for ic in 0..<table.columns.count
      {
        switch plotInfo.columnTypes[ic]
        {
        case Boxes_ColumnType.datetime, Boxes_ColumnType.text:
          line.append(table.columns[ic].strValues[iv])
        default:
          line.append(table.columns[ic].numValues[iv].description)
        }
      }
      rows.append(TableDataRow(id: iv, text: line))
    }
  }
}

class TableDataRow: Identifiable
{
  let id: Int
  let text: [String]
  
  init (id: Int, text: [String])
  {
    self.id   = id
    self.text = text
  }
}
