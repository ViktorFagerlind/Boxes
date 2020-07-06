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

class DataEngineProxy
{
  let client: Boxes_DataEngineClient
  let group: EventLoopGroup

  init (ip: String, port: Int)
  {
    group = MultiThreadedEventLoopGroup(numberOfThreads: 1)
    client = makeClient(ip: "vfhome.asuscomm.com", port: 51234, group: group)
  }
  
  deinit
  {
    try? client.channel.close().wait()
    try? group.syncShutdownGracefully()
  }

  func executeQuery(query: String) -> Boxes_Table
  {

    let query: Boxes_Query = .with {$0.q = query}
    let call = client.executeQuery(query)
    let table: Boxes_Table
    
    do
    {
      print("ExecuteQuery")
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

func makeClient(ip: String, port: Int, group: EventLoopGroup) -> Boxes_DataEngineClient
{
  let channel = ClientConnection.insecure(group: group).connect(host: ip, port: port)

  return Boxes_DataEngineClient(channel: channel)
}

func executeQuery(client: Boxes_DataEngineClient) -> Boxes_Table
{
  print("ExecuteQuery")

  let query: Boxes_Query = .with
  {
    $0.q = "select * from all_activities"
  }

  let call = client.executeQuery(query)
  let table: Boxes_Table
  
  do
  {
    table = try call.response.wait()
  }
  catch
  {
    print("RPC failed: \(error)")
    table = Boxes_Table()
  }
  
  return table
}

func test()
{
  let group = MultiThreadedEventLoopGroup(numberOfThreads: 1)
  defer {
    try? group.syncShutdownGracefully()
  }

  // Make a client, make sure we close it when we're done.
  let client = makeClient(ip: "vfhome.asuscomm.com", port: 51234, group: group)
  defer
  {
    try? client.channel.close().wait()
  }

  let response = executeQuery(client: client)
}

