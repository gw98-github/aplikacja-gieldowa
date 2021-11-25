import { Component, OnInit } from '@angular/core';
import { StockDataService } from '../services/stock-data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  popularList: any = [];

  constructor(private stockDataService: StockDataService) { }

  ngOnInit(): void {
    this.stockDataService
      .getPopularCompanies()
      .subscribe((response) => {
        //next() callback
        this.popularList = response.popular;
        console.log(this.popularList)

      })
  }


}
