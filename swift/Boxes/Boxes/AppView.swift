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
  let title: String
  
  @ObservedObject var queryModel: QueryModel
  @State private var showingSheet = false
  
  init(title: String, queryModel: QueryModel)
  {
    self.title = title
    self.queryModel = queryModel
  }
  
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
    .sheet(isPresented: $showingSheet)
    {
      TableView(title: self.title, rows: self.queryModel.rows)
    }
    .onAppear
    {
      self.queryModel.loadFromDataEngine()
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
    AppView(title: "Top 200m swims",
            queryModel: QueryModel(query: "SELECT total_elapsed_time FROM swim_lengths LIMIT 30",
                                   columnTypes: [Boxes_ColumnType.real],
                                   y_col: 0))
  }
}
