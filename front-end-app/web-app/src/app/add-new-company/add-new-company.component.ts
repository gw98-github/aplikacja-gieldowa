import { Component, OnInit } from '@angular/core';
import { StockDataService } from '../services/stock-data.service';

@Component({
  selector: 'app-add-new-company',
  templateUrl: './add-new-company.component.html',
  styleUrls: ['./add-new-company.component.css'],
})
export class AddNewCompanyComponent implements OnInit {
  candidates: any;

  constructor(private stockDataService: StockDataService) {}

  ngOnInit(): void {
    this.stockDataService.getCandidatesList().subscribe((response) => {
      this.candidates = response.candidates;
    });
  }
}
