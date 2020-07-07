//
//  AppView.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-06.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import SwiftUI

struct AppView: View
{
  var body: some View
  {
    TabView
    {
      ContentView()
        .tabItem
        {
          Text("Tab Label 1")
        }
      GraphView()
        .tabItem
        {
          Text("Tab Label 2")
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
