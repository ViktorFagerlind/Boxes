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

class Table: ObservableObject // TODO: Observable needed??
{
  var loaded: Bool = false
  
  let name: String
  let query: String
  let columnTypes: [Boxes_ColumnType]
  let columnNames: [String]
  
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
  }
}

