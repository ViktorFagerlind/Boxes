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
  let chart: Chart
  @State private var showingSheet = false
  
  var body: some View
  {
    VStack
    {
      Text(chart.name)
        .font(.headline)
      
      ChartsCombinedView(chart: chart)

      Button("Show chart data")
      {
        self.showingSheet.toggle()
      }
    }
    .sheet(isPresented: $showingSheet)
    {
      TableView(chart: self.chart)
    }
  }
}

func createRows(plot: Plot) -> [IdStringPair]
{
  var pairs: [IdStringPair] = []
  
  for (i,(date, value)) in zip(plot.getXvalues(), plot.getYValues()).enumerated()
  {
    pairs.append(IdStringPair(id: i, first: date, second: value.description))
  }
  
  return pairs
}

class IdStringPair: Identifiable
{
  let id: Int
  let first: String
  let second: String

  init (id: Int, first: String, second: String)
  {
    self.id     = id
    self.first  = first
    self.second = second
  }
}

class PlotTable: Identifiable
{
  let id = UUID()
  let name: String
  let rows: [IdStringPair]

  init (name: String, rows: [IdStringPair])
  {
    self.name = name
    self.rows = rows
  }
}

struct TableView: View
{
  @Environment(\.presentationMode) var presentation

  let title: String
  var plotTables: [PlotTable] = []
  
  init(chart: Chart)
  {
    title = chart.name
    
    for plot in chart.plots
    {
      let plotTable = PlotTable(name: plot.name, rows: createRows(plot: plot))
      plotTables.append(plotTable)
    }
  }

  var body: some View
  {
    VStack
    {
      Text(title)
      TabView
      {
        ForEach(plotTables)
        { plotTable in
          VStack
          {
            List(plotTable.rows)
            { stringPair in
              HStack
              {
                Text(stringPair.first)
                  .font(.body)
                  .multilineTextAlignment(.trailing)
                  .frame(width: 100.0)
                Text(stringPair.second)
                  .font(.body)
                  .multilineTextAlignment(.trailing)
                  .frame(width: 140.0)
              }
            }
          }
            .font(.title)
            .tabItem
            {
              Image(systemName: "table")
              Text(plotTable.name)
            }
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
