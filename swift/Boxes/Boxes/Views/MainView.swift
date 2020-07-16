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
  var body: some View
  {
    TabView
    {
      ChartsListView()
        .font(.title)
        .tabItem
        {
          Image(systemName: "chart.bar")
          Text("Charts")
        }
      TablesListView()
        .font(.title)
        .tabItem
        {
          Image(systemName: "table")
          Text("Tables")
        }
    }
  }
}


struct TablesListView: View
{
  var body: some View
  {
    NavigationView
    {
      List
      {
        ForEach(TableCollection.singleton.tables)
        { table in
          NavigationLink(destination: TableView(table: table))
          {
            Text(table.name)
              .font(.headline)
          }
        }
      }
      .environment(\.defaultMinListRowHeight, 30)
      .navigationBarTitle("")
      .navigationBarHidden(true)
    }
  }
}


struct MainView_Previews: PreviewProvider
{
  static var previews: some View
  {
    MainView()
    .environment(\.colorScheme, .dark)
  }
}
