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
  // TODO: Should be able to get it from query result instead of duplicating everything as strings...
  @Published private(set) var rows: [TableDataRow] = []

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
    
    updateRows()
  }
  
  private func updateRows ()
  {
    for iv in 0..<contents.columns[0].strValues.count
    {
      var line: [String] = []
      for ic in 0..<contents.columns.count
      {
        switch columnTypes[ic]
        {
        case Boxes_ColumnType.datetime, Boxes_ColumnType.text:
          line.append(contents.columns[ic].strValues[iv])
        default:
          line.append(contents.columns[ic].numValues[iv].description)
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


/*

class QueryModel: ObservableObject
{
  let plotInfo: Chart
  var loaded: Bool = false

  // TODO: Should be able to get it from query result instead of duplicating everything as strings...
  @Published private(set) var rows: [TableDataRow] = []

  var table: Boxes_Table = Boxes_Table()
  
  init(plotInfo: Chart)
  {
    self.plotInfo = plotInfo
  }
  
  var setCount: Int {get {return plotInfo.sets.count}}
  
  // TODO: Only support dates string/dates this way...
  func getXdata() -> [String]
  {
    loadFromDataEngine()
    
    return table.columns[plotInfo.x_col].strValues
  }

  func getYdata(set: Int) -> [Double]
  {
    loadFromDataEngine()
    
    return table.columns[plotInfo.sets[set].y_col].numValues
  }

  func getPlotName(set: Int) -> String
  {
    loadFromDataEngine()
    
    return plotInfo.columnNames[plotInfo.sets[set].y_col]
  }

  func loadFromDataEngine()
  {
    if loaded {return}
    loaded = true
    
    print("Loading: \(plotInfo.query)")

    table = DataEngineProxy.singleton.executeQuery(query: plotInfo.query, columnTypes: plotInfo.columnTypes)
    
    updateRows()
  }
  
  private func updateRows ()
  {
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
*/

