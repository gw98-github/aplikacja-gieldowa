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
    this.multi = this.stockDataService.getStaticData();
  }
  ngOnInit(): void {}

  public onSelect(event: any): void {}

  public onRefresh(): void {}
}
