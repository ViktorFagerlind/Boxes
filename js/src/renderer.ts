'use strict'
import * as Plotly from 'plotly.js';

let canvas = div("canvas", "canvas");
document.body.append(canvas);

// Generate some plots
for (let i = 0; i < 4; ++i)
{
  let plotItem = div(i.toString(), "plot-item");
  canvas.append(plotItem);  

  let arr = Array.from({length: 3}, () => Math.random());
  plot(plotItem, arr);
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
