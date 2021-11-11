import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { StockDataService } from '../services/stock-data.service';

import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';

export interface CompanyElement {
  name: string;
  week_avg: number;
}

@Component({
  selector: 'app-companies-list',
  templateUrl: './companies-list.component.html',
  styleUrls: ['./companies-list.component.css'],
})
export class CompaniesListComponent implements OnInit {
  companies: Array<any> = [];
  displayedColumns: string[] = ['number', 'name', 'week_avg', 'details'];
  dataSource = new MatTableDataSource(this.companies);

  constructor(
    private stockDataService: StockDataService,
    private router: Router
  ) {
    this.stockDataService.getCompaniesList().subscribe((response) => {
      this.companies = response.companies;
      this.dataSource.data = this.companies;
      console.log(this.dataSource);
    });
  }
  ngOnInit(): void {}

  openCompanyPage(companyName: any) {
    // this.router.navigate(['/' + companyName]);
    this.router.navigate(['/company/' + companyName]);
  }
}
