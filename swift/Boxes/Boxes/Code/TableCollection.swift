//
//  QueryModels.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-07.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Foundation
import Yaml

class TableCollection
{
  var tables: [Table] = []

  static let singleton = TableCollection()
  
  func getTable(name: String) -> Table?
  {
    return tables.first(where: {$0.name == name})
  }
  
  private init()
  {
    let path = Bundle.main.path(forResource: "tables_and_charts", ofType: "yaml")
    let fm = FileManager()
    let content = fm.contents(atPath: path!)
    let yaml = try! Yaml.load(String(data: content!, encoding: String.Encoding.utf8)!)

    for tableYaml in yaml["tables"].array!
    {
      var columnNames: [String] = []
      var columnTypes: [Boxes_ColumnType] = []

      for col in tableYaml["columns"].array!
      {
        var type: Boxes_ColumnType = Boxes_ColumnType.unused
        switch col["type"].string!
        {
          case "REAL":      type = Boxes_ColumnType.real
          case "DATETIME":  type = Boxes_ColumnType.datetime
          case "INTEGER":   type = Boxes_ColumnType.integer
          default:          type = Boxes_ColumnType.text
        }
        
        columnNames.append(col["name"].string!)
        columnTypes.append(type)
      }
      
      let table: Table = Table(name:  tableYaml["name"].string!,
                               query: tableYaml["query"].string!,
                               columnNames: columnNames,
                               columnTypes: columnTypes)

      tables.append(table)
    }
  }
}



class Table: Identifiable //ObservableObject
{
  var loaded: Bool = false
  
  let id = UUID()
  let name: String
  let query: String
  let columnTypes: [Boxes_ColumnType]
  let columnNames: [String]
  
  private var textRows: [TableTextRow] = []
  
  var rows: [TableTextRow] {get {loadContents(); return textRows}}

  private var contents: Boxes_Table = Boxes_Table()
  
  init(name: String, query: String, columnNames: [String], columnTypes: [Boxes_ColumnType])
  {
    self.name = name
    self.query = query
    self.columnNames = columnNames
    self.columnTypes = columnTypes
  }
  
  func getColumnType(columnName: String) -> Boxes_ColumnType
  {
    let i = columnNames.firstIndex(of: columnName)
    
    return columnTypes[i!]
  }
  
  func getColumnData(columnName: String) -> [String]
  {
    let i = columnNames.firstIndex(of: columnName)
    
    loadContents() // TODO: A better way to do this?
    
    return contents.columns[i!].strValues
  }
  
  func getColumnData(columnName: String) -> [Double]
  {
    let i = columnNames.firstIndex(of: columnName)
    
    loadContents() // TODO: A better way to do this?
    
    return contents.columns[i!].numValues
  }
  
  func loadContents()
  {
    if loaded {return}
    loaded = true
    
    print("Loading: \(query)")

    contents = DataEngineProxy.singleton.executeQuery(query: query, columnTypes: columnTypes)
    
    createRows()
  }
  
  func getRowCount() -> Int
  {
    return max(contents.columns[0].numValues.count, contents.columns[0].strValues.count)
  }

  func createRows()
  {
    let nofRows = getRowCount()
    
    for i in 0..<nofRows
    {
      var row: [String] = []
      for c in contents.columns
      {
        if c.numValues.count == 0
        {
          row.append(c.strValues[i])
        }
        else
        {
          row.append(String(format: "%.2f", c.numValues[i]))
        }
      }
      textRows.append(TableTextRow(id: i, items: row))
    }
    
  }
}

// Mostly to be able to show the table
class TableTextRow: Identifiable
{
  let id: Int
  let items: [String]

  init (id: Int, items: [String])
  {
    self.id    = id
    self.items = items
  }
}
