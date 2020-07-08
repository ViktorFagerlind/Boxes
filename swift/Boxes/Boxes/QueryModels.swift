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

  @Published private(set) var rows: [TableDataRow] = []
  @Published private(set) var y_vals: [Double] = []

  var table: Boxes_Table = Boxes_Table()
    
  init(query: String, columnTypes: [Boxes_ColumnType])
  {
    self.query = query
    self.columnTypes = columnTypes
  }
  
  func load()
  {
    table = DataEngineProxy.singleton.executeQuery(query: query, columnTypes: columnTypes)
    y_vals = table.columns[1].numValues
    
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
