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

let canvas = document.getElementById("canvas");
canvas.setAttribute("class", "container");

let plotItem1 = div("1");
plotItem1.setAttribute("class", "plot-item");

let plotItem2 = div("2");
plotItem1.setAttribute("class", "plot-item");

canvas.append(plotItem1);
canvas.append(plotItem2);

let arr = Array.from({length: 3}, () => Math.random());

data_engine_services.GetPlotData({name: 'swim.csv'}, function(err: any, response: any) {
  console.log('Received plot data from rpc:', response.value);
  arr[1] = response.value
});

plot(plotItem1, arr);
plot(plotItem2, arr);

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

function div(id: string) : HTMLElement
{
  let elem = document.createElement("div");
  elem.id = id;

  return elem;
}
