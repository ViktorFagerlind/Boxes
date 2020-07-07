//
//  TableRow.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-06.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI

struct TableRow: View
{
  var tableDataRow: TableDataRow
  
  var body: some View
  {
    HStack
    {
      Text(tableDataRow.text[0])
        .multilineTextAlignment(.trailing)
        .frame(width: 100.0)
      Text(tableDataRow.text[1])
        .multilineTextAlignment(.trailing)
        .frame(width: 140.0)
    }
  }
}

struct TableRow_Previews: PreviewProvider
{
  static var previews: some View
  {
    TableRow(tableDataRow: TableDataRow(id: 0, text: ["2016-02", "196.734"]))
  }
}
