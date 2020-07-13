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
  let text_w: CGFloat = 200
  let text_h: CGFloat = 70

  var body: some View
  {
    NavigationView
    {
      List
      {
        ForEach(PlotInfoCollection.singleton.plots.sorted(by: {$0.name > $1.name}), id: \.self)
        { plotInfo in
          NavigationLink(destination: PlotView(queryModel: QueryModel(plotInfo: plotInfo)))
          {
            PlotNavigationView(plotInfo: plotInfo)
          }
        }
      }
      .navigationBarTitle("")
      .navigationBarHidden(true)
    }
  }
}

struct PlotNavigationView: View
{
  let text_w: CGFloat = 200
  let text_h: CGFloat = 70

  let plotInfo: PlotInfo
  
  var body: some View
  {
    VStack
    {
      ZStack(alignment: .bottomLeading)
      {
        Image(plotInfo.category)
          .resizable()
          .aspectRatio(contentMode: .fill)
          .frame(width:300, height: 100)
          .cornerRadius(20)
          .shadow(color: Color(red:0.5, green:0.5, blue:0.5), radius: 5, x: 5, y:5)
        ZStack(alignment: .center)
        {
          Rectangle()
            .frame(width: self.text_w*1.2, height: self.text_h*1.2)
            .opacity(0.9)
            .foregroundColor(.black)
            .blur(radius: self.text_h/3)
          Text(plotInfo.name)
            .multilineTextAlignment(.center)
            .frame(width: self.text_w)
            .foregroundColor(.white)
            .font(.subheadline)
        }
        .frame(width: 190.0, height: 40.0)
      }
      .padding(10)
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
