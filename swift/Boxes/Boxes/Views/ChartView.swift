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

struct ChartView: View
{
  // TODO: Doubt id ObservedObject is really needed
  let chart: Chart
  @State private var showingSheet = false
  
  var body: some View
  {
    VStack
    {
      // TODO: Kind needed?
      GraphView(chart: chart, kind: chart.plots[0].kind)

      Button("Show table data")
      {
        self.showingSheet.toggle()
      }
    }
    .sheet(isPresented: $showingSheet)
    {
      // TODO: Totally wrong!
      Text("TODO!!")
      //TableView(title: self.chart.name, rows: self.chart.r)
    }
    /*.onAppear
    {
      self.queryModel.loadFromDataEngine()
    }*/
  }
}

struct GraphView: View
{
  let chart: Chart
  
  @State var kind: String
  
  var body: some View
  {
    VStack
    {
      ChartsCombinedView(chart: chart)
      /*
      // TODO: Plot all sets, not just the first...
      if kind == "bar"
      {
        ChartsBarView(dates:  chart.plots[0].getXvalues(),
                      values: chart.plots[0].getYValues(),
                      color:  chart.plots[0].color,
                      label:  chart.plots[0].yColumn)
      }
      else
      {
        ChartsCombinedView(dates:  chart.plots[0].getXvalues(),
                           values: chart.plots[0].getYValues(),
                           color:  chart.plots[0].color,
                           label:  chart.plots[0].yColumn)
      }
 */
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
    ChartView(chart: ChartCollection.singleton.charts[0])
  }
}
