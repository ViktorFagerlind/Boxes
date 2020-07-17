//
//  PlotInfo.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-09.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Foundation
import Charts
import Yaml

func getBool(yaml: Yaml) -> Bool
{
  return yaml.bool == nil ? false : yaml.bool!
}

class ChartCollection
{
  static let singleton = ChartCollection()
  
  var charts: [Chart] = []
  
  private init()
  {
    let path = Bundle.main.path(forResource: "tables_and_charts", ofType: "yaml")
    let fm = FileManager()
    let content = fm.contents(atPath: path!)
    let yaml = try! Yaml.load(String(data: content!, encoding: String.Encoding.utf8)!)

    for chartYaml in yaml["charts"].array!
    {
      var plots: [Plot] = []
      for plotYaml in chartYaml["plots"].array!
      {
        let plot = Plot(table: plotYaml["table"].string!,
                        kind: plotYaml["kind"].string!,
                        xColumn: plotYaml["x-column"].string!,
                        yColumn: plotYaml["y-column"].string!,
                        color: colorFromString(plotYaml["color"].string),
                        filled: getBool(yaml: plotYaml["filled"]),
                        circles: getBool(yaml: plotYaml["circles"]))
        plots.append(plot)
      }

      let chart: Chart = Chart(name: chartYaml["name"].string!,
                               category: chartYaml["category"].string!,
                               plots: plots)
      
      charts.append(chart)
    }
  }
}

struct Chart: Hashable
{
  let name: String
  let category: String

  let plots: [Plot]
  
}

struct Plot: Hashable
{
  let table:   String
  let kind:    String
  let xColumn: String
  let yColumn: String
  let color:   NSUIColor
  let filled:  Bool
  let circles: Bool

  var name: String {get {table + " - " + yColumn}}

  func getXvalues() -> [String]
  {
    return TableCollection.singleton.getTable(name: table)!.getColumnData(columnName: xColumn)
  }
  
  func getYValues() -> [Double]
  {
    return TableCollection.singleton.getTable(name: table)!.getColumnData(columnName: yColumn)
  }
}

func colorFromString(_ colorString: String?) -> UIColor
{
  switch colorString
  {
  case "black":     return UIColor.black
  case "darkGray":  return UIColor.darkGray
  case "lightGray": return UIColor.lightGray
  case "white":     return UIColor.white
  case "gray":      return UIColor.gray
  case "red":       return UIColor.red
  case "green":     return UIColor.green
  case "blue":      return UIColor.blue
  case "cyan":      return UIColor.cyan
  case "yellow":    return UIColor.yellow
  case "magenta":   return UIColor.magenta
  case "orange":    return UIColor.orange
  case "purple":    return UIColor.purple
  case "brown":     return UIColor.brown
  default:
    let rgb: UInt? = colorString == nil ? nil : UInt(colorString!, radix: 16)
    
    if rgb == nil
    {
      return UIColor(red:   CGFloat.random(in: 0.2...1.0),
                     green: CGFloat.random(in: 0.2...1.0),
                     blue:  CGFloat.random(in: 0.2...1.0),
                     alpha: 0.8)
    }
    else
    {
      return colorFromRGB(rgb: rgb!)
    }
  }
}


func colorFromRGB(rgb: UInt) -> UIColor
{
    return UIColor(
        red:    CGFloat((rgb & 0xFF000000) >> 24) / 255.0,
        green:  CGFloat((rgb & 0x00FF0000) >> 16) / 255.0,
        blue:   CGFloat((rgb & 0x0000FF00) >>  8) / 255.0,
        alpha:  CGFloat (rgb & 0x000000F0)        / 255.0
    )
}
