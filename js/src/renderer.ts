'use strict'
import * as Plotly from 'plotly.js';

let canvas = document.getElementById("canvas");
canvas.setAttribute("class", "container");

let plotItem1 = div("1");
plotItem1.setAttribute("class", "plot-item");

let plotItem2 = div("2");
plotItem1.setAttribute("class", "plot-item");

canvas.append(plotItem1);
canvas.append(plotItem2);

let arr = Array.from({length: 3}, () => Math.random());

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
