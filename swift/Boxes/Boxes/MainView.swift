//
//  MainView.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-08.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI

struct MainView: View
{
  struct Info: Hashable
  {
    var title: String
    var query: String
    var columnTypes: [Boxes_ColumnType]
    var y_col: Int
  }
  
  let infos: [Info] = [
    Info(title: "Top 100m swims",
         query: """
         SELECT strftime("%Y-%m-%d", r.startTimeLocal), min(l.total_elapsed_time)
         FROM swim_lengths l
         LEFT JOIN all_activities r ON l.activityId = r.activityId
         WHERE l.total_elapsed_time > 73 AND l.total_elapsed_time < 140 AND l.total_distance == 100
         GROUP BY strftime("%Y-%m", r.startTimeLocal)
         ORDER BY r.startTimeLocal
         """,
         columnTypes: [Boxes_ColumnType.datetime, Boxes_ColumnType.real],
         y_col: 1),
    Info(title: "Top 200m swims",
         query: """
         SELECT strftime("%Y-%m", r.startTimeLocal), min(l.total_elapsed_time)
         FROM swim_lengths l
         LEFT JOIN all_activities r ON l.activityId = r.activityId
         WHERE l.total_elapsed_time > 150 AND l.total_elapsed_time < 360 AND l.total_distance == 200
         GROUP BY strftime("%Y-%m", r.startTimeLocal)
         ORDER BY r.startTimeLocal
         """,
         columnTypes: [Boxes_ColumnType.datetime, Boxes_ColumnType.real],
         y_col: 1)
  ]
  
  
  var body: some View
  {
    TabView()
    {
      ForEach(infos, id: \.self)
      { info in
        AppView(title: info.title,
                queryModel: QueryModel(query: info.query,
                                       columnTypes: info.columnTypes,
                                       y_col: info.y_col))
          .tabItem { Text(info.title) }
          .tag(info.title)
      }
    }
    
  }
}

struct MainView_Previews: PreviewProvider
{
  static var previews: some View
  {
    MainView()
  }
}
