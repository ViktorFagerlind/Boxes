//
//  DataEngineInterface.swift
//  Boxes
//
//  Created by Viktor Fägerlind on 2020-07-05.
//  Copyright © 2020 ViktorApps. All rights reserved.
//

import Foundation
import GRPC
import NIO
import Logging

func makeClient(ip: String, port: Int, group: EventLoopGroup) -> Boxes_DataEngineClient
{
  let channel = ClientConnection.insecure(group: group).connect(host: ip, port: port)

  return Boxes_DataEngineClient(channel: channel)
}


class DataEngineProxy
{
  let client: Boxes_DataEngineClient
  let group: EventLoopGroup
  
  static let singleton = DataEngineProxy(ip: "vfhome.asuscomm.com", port: 51234)

  private init (ip: String, port: Int)
  {
    group = MultiThreadedEventLoopGroup(numberOfThreads: 1)
    client = makeClient(ip: ip, port: port, group: group)
  }
  
  deinit
  {
    try? client.channel.close().wait()
    try? group.syncShutdownGracefully()
  }

  func executeQuery(query: String, columnTypes: [Boxes_ColumnType]) -> Boxes_Table
  {
    let query: Boxes_Query = .with {$0.q = query; $0.columnTypes=columnTypes}
    let call = client.executeQuery(query)
    let table: Boxes_Table
    
    do
    {
      print("ExecuteQuery: \(query.q)")
      table = try call.response.wait()
    }
    catch
    {
      print("RPC failed: \(error)")
      table = Boxes_Table()
    }
    
    return table
  }
}


