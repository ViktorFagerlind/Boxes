//
//  GraphView.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-07.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI
import SwiftUICharts
import Charts

struct GraphView: View
{
  var body: some View
  {
    LineView(data: [8,23,54,32,12,37,7,23,43], title: "200m swims", legend: "Time")
  }
}

struct GraphView_Previews: PreviewProvider
{
  static var previews: some View
  {
    GraphView()
  }
}
