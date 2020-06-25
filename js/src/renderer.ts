'use strict'
import * as Plotly from 'plotly.js';
import { Framework } from './framework';
import { Internals } from './internals';
import { UIComponents } from './ui_components';

const tableName = 'swim.csv';
const dataEngine = new Internals.DataEngine('localhost:50053');

let root = Framework.div("root");
document.body.append(root);

let sidebar = new UIComponents.SideBar();
sidebar.render(root);

let canvas = Framework.div("canvas");
root.append(canvas);

// Generate some plots
for (let i = 0; i < 4; ++i)
{
  let plotItem = Framework.div("plot-item");

  let plotDataResponseHandler = (response: any) => {
    let arr = Array.from({ length: 3 }, () => { return Math.random()*20.0 + response.value });
    plot(plotItem, arr);
   
    canvas.append(plotItem);
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

  Plotly.newPlot(elem, plotData, {}, { responsive: true });
}