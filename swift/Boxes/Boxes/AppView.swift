//
//  AppView.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-06.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI
import Combine
import SwiftUICharts

struct AppView: View
{
  let title: String = "Top 200m swims"
  
  @ObservedObject var queryModel: QueryModel = QueryModel(
    query: """
      SELECT strftime("%Y-%m", r.startTimeLocal), min(l.total_elapsed_time)
      FROM swim_lengths l
      LEFT JOIN all_activities r ON l.activityId = r.activityId
      WHERE l.total_elapsed_time > 150 AND l.total_elapsed_time < 360 AND l.total_distance == 200
      GROUP BY strftime("%Y-%m", r.startTimeLocal)
      ORDER BY r.startTimeLocal
      """,
    columnTypes: [Boxes_ColumnType.datetime, Boxes_ColumnType.real])
  
  @State private var showingSheet = false
  
  var body: some View
  {
    VStack
    {
      GraphView(title: self.title, data: self.queryModel.y_vals)
      
      Button("Show table data")
      {
        self.showingSheet.toggle()
      }
    }
    .onAppear
    {
      self.queryModel.load()
    }
    .sheet(isPresented: $showingSheet)
    {
      TableView(title: self.title, rows: self.queryModel.rows)
    }
  }
}

struct GraphView: View
{
  let title: String
  let data: [Double]
  
  var body: some View
  {
    LineView(data: data, title: self.title, legend: "Time")
  }
}

struct TableView: View
{
  @Environment(\.presentationMode) var presentation

  let title: String
  
  let rows: [TableDataRow]

  var body: some View
  {
    VStack
    {
      Text(self.title)
        .font(.title)
      List (rows)
      {
        tableDataRow in TableRow(tableDataRow: tableDataRow)
      }
      Button("Dismiss")
      {
        self.presentation.wrappedValue.dismiss()
      }
    }
  }
}

struct AppView_Previews: PreviewProvider
{
  static var previews: some View
  {
    AppView()
  }
}
