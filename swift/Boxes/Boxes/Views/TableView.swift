//
//  TableView.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-16.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI

struct TableView: View
{
  let table: Table
  
  var body: some View
  {
    VStack(alignment: .center, spacing: 0)
    {
      List
      {
        Section(header:
          VStack
          {
            TableRowView(cells: self.table.columnNames)
              .font(Font.body.bold())
            TableRowView(cells: self.table.columnTypes.map({return "(\($0))"}))
              .font(Font.body)
          })
        {
          ForEach(table.rows)
          { row in
            TableRowView(cells: row.items)
          }
          .font(Font.body)
        }
      }
      .environment(\.defaultMinListRowHeight, 30)
    }
    .navigationBarTitle(Text(table.name), displayMode: .inline)
  }
}

struct TableRowView: View
{
  let cells: [String]
  
  var body: some View
  {
    HStack
    {
      ForEach(cells, id: \.self)
      { cell in
        Text(cell)
          .multilineTextAlignment(.leading)
          .frame(width: 100.0, height: 20.0)
      }
    }
  }
}

struct TableView_Previews: PreviewProvider
{
    static var previews: some View
    {
      TableView(table: TableCollection.singleton.tables[0])
    }
}
