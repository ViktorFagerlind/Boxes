//
//  ContentView.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-05.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI

struct ContentView: View
{
  let tableData: TableData

  init()
  {
    tableData = DataEngineProxy.singleton.executeQuery(query: """
      SELECT strftime("%Y-%m", r.startTimeLocal), min(l.total_elapsed_time)
      FROM swim_lengths l
      LEFT JOIN all_activities r ON l.activityId = r.activityId
      WHERE l.total_elapsed_time > 150 AND l.total_elapsed_time < 360 AND l.total_distance == 200
      GROUP BY strftime("%Y-%m", r.startTimeLocal)
      ORDER BY r.startTimeLocal
      """)
  }
  
  var body: some View
  {
    VStack
    {
      Text("Top 200m swims!")
        .font(.title).fontWeight(.heavy)
      
      List (tableData.rows)
      {
        tableDataRow in TableRow(tableDataRow: tableDataRow)
      }
    }
  }
}

struct ContentView_Previews: PreviewProvider
{
    static var previews: some View
    {
      ContentView()
    }
}
