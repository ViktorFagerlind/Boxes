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
  let query: String
  let columnTypes: [Boxes_ColumnType]
  let y_col: Int
  var loaded: Bool = false

  @Published private(set) var rows: [TableDataRow] = []
  @Published private(set) var y_vals: [Double] = []

  var table: Boxes_Table = Boxes_Table()
    
  init(query: String, columnTypes: [Boxes_ColumnType], y_col: Int)
  {
    self.query = query
    self.columnTypes = columnTypes
    self.y_col = y_col
    
    loadFromDataEngine() // TODO: Should not be needed, instead invoked from onAppear. But seems to be a bug when running on device.
  }
  
  func loadFromDataEngine()
  {
    if loaded {return}
    loaded = true
    
    print("Loading: \(query)")

    table = DataEngineProxy.singleton.executeQuery(query: query, columnTypes: columnTypes)
    y_vals = table.columns[y_col].numValues
    
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
        switch columnTypes[ic]
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
