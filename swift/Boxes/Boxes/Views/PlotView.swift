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

struct PlotView: View
{
  // TODO: Doubt id ObservedObject is really needed
  @ObservedObject var queryModel: QueryModel
  @State private var showingSheet = false
  
  init(queryModel: QueryModel)
  {
    self.queryModel = queryModel
  }
  
  var body: some View
  {
    VStack
    {
      GraphView(queryModel: self.queryModel, kind: queryModel.plotInfo.sets[0].kind)

      Button("Show table data")
      {
        self.showingSheet.toggle()
      }
    }
    .sheet(isPresented: $showingSheet)
    {
      TableView(title: self.queryModel.plotInfo.name, rows: self.queryModel.rows)
    }
    /*.onAppear
    {
      self.queryModel.loadFromDataEngine()
    }*/
  }
}

struct GraphView: View
{
  let queryModel: QueryModel
  
  @State var kind: String
  
  var body: some View
  {
    VStack
    {
      // TODO: Plot all sets, not just the first...
      if kind == "bar"
      {
        ChartsBarView(dates: queryModel.getXdata(),
                      values: queryModel.getYdata(set: 0),
                      color: queryModel.plotInfo.sets[0].color,
                      label: queryModel.getPlotName(set: 0))
      }
      else
      {
        ChartsLineView(dates: queryModel.getXdata(),
                       values: queryModel.getYdata(set: 0),
                       color: queryModel.plotInfo.sets[0].color,
                       label: queryModel.getPlotName(set: 0))
      }
    }
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
        tableDataRow in
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
    PlotView(queryModel: QueryModel(plotInfo: PlotInfoCollection.singleton.plots[0]))
  }
}
