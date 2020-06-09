'use strict'
import * as Plotly from 'plotly.js';
import { Framework } from './framework';
import { Internals } from './internals';

const tableName = 'swim.csv';
const dataEngine = new Internals.DataEngine('localhost:50053');

let canvas = Framework.div("canvas");
document.body.append(canvas);

// Generate some plots
for (let i = 0; i < 4; ++i)
{
  let plotItem = Framework.div("plot-item");
  canvas.append(plotItem);  

  let plotDataResponseHandler = (response: any) => {
    let arr = Array.from({ length: 3 }, () => { return Math.random()*20.0 + response.value });
    plot(plotItem, arr);
  }

  dataEngine.GetPlotData(tableName, plotDataResponseHandler)
}

function plot(elem: HTMLElement, data: number[])
{
  let plotData: Plotly.Data[] = [
    {
      x: ['lap_1', 'lap_2', 'lap_3'],
      y: data,
      type: 'bar',
    }
  ];

  Plotly.newPlot(elem, plotData);
}
