import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'submarine-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss']
})
export class LineChartComponent {
  lineChartData: ChartDataSets[] = [
    { data: [85, 72, 78, 75, 77, 75], label: 'loss', fill: false}
  ];

  lineChartLabels: Label[] = ['10', '20', '30', '40', '50', '60'];

  lineChartOptions = {
    responsive: true
  };

  lineChartColors: Color[] = [
    {
      borderColor: 'black'
    }
  ];

  lineChartLegend = true;
  lineChartPlugins = [];
  lineChartType = 'line';
}
