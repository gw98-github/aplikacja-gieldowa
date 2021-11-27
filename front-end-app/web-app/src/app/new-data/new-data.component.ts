import { Component, OnInit } from '@angular/core';
import { StockDataService } from '../services/stock-data.service';

@Component({
  selector: 'app-new-data',
  templateUrl: './new-data.component.html',
  styleUrls: ['./new-data.component.css'],
})
export class NewDataComponent implements OnInit {
  constructor(private stockDataService: StockDataService) {}

  ngOnInit(): void {}

  csvInputChange(fileInputEvent: any) {
    // console.log(fileInputEvent.target.files[0]);
    this.stockDataService
      .postFileWithData(fileInputEvent.target.files[0])
      .subscribe((response) => {
        console.log(response);
      });
  }
}
