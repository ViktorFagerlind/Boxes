'use strict'
import * as Plotly from 'plotly.js';

var PROTO_PATH = `${__dirname}/../../protos/table.proto`;

var grpc = require('grpc');
var protoLoader = require('@grpc/proto-loader');

var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
var tables_proto_package = grpc.loadPackageDefinition(packageDefinition).tableservices;

var data_engine_services = new tables_proto_package.DataEngine('localhost:50053', grpc.credentials.createInsecure());

let canvas = div("canvas", "canvas");
document.body.append(canvas);

// Generate some plots
for (let i = 0; i < 4; ++i)
{
  let plotItem = div(i.toString(), "plot-item");
  canvas.append(plotItem);  

  data_engine_services.GetPlotData({name: 'swim.csv'}, function(err: any, response: any) {
    console.log('Received plot data from rpc:', response.value);
    let arr = Array.from({length: 3}, () => {return Math.random()*20.0+response.value});
    plot(plotItem, arr);
  });

}

function plot(elem: HTMLElement, data: number[])
{
  let plotData: Plotly.Data[] = [
    {
      x: ['giraffes', 'orangutans', 'monkeys'],
      y: data,
      type: 'bar',
    }
  ];

  Plotly.newPlot(elem, plotData);
}

function div(id: string, classSelector?: string) : HTMLElement
{
  let elem = document.createElement("div");
  elem.setAttribute("id", id);

  if (classSelector)
  {
    elem.setAttribute("class", classSelector);
  }

  return elem;
}
