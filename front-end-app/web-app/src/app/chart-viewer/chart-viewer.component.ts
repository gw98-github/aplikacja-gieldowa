import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { HistoricalData } from '../model';
import { StockDataService } from '../services/stock-data.service';

@Component({
  selector: 'app-chart-viewer',
  templateUrl: './chart-viewer.component.html',
  styleUrls: ['./chart-viewer.component.css'],
})
export class ChartViewerComponent implements OnInit {
  historicalData: Observable<HistoricalData[]> =
    this.stockDataService.historicalData;
  multi: any[];
  data: any;

  viewSize: [number, number] = [800, 360];

  // options
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showXAxisLabel = true;
  xAxisLabel = 'Data';
  showYAxisLabel = true;
  yAxisLabel = 'Wartość';
  scale = true;

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA'],
  };

  constructor(private stockDataService: StockDataService) {
    this.multi = [];
    this.stockDataService.getData().subscribe((response) => {
      //next() callback
      this.data = response.data;
      this.data = this.createList(this.data);
      this.multi = [
        {
          name: 'Wartość',
          series: this.data,
        },
      ];
    });
  }
  ngOnInit(): void {}

  public onSelect(event: any): void {}

  public onRefresh(): void {}

  createList(object: any) {
    let data: Array<{ name: string; value: number }> = [];
    const keys = Object.keys(object);
    const values = Object.values(object);
    for (let n = 0; n < keys.length; n++) {
      data.push({ name: keys[n], value: values[n] as number });
    }

    return data;
  }
}
