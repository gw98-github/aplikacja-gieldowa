import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { StockDataService } from '../services/stock-data.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';

export interface CompanyElement {
  name: string;
  symbol: string;
  growing: string;
  growing_by: number;
  value: number;
}

@Component({
  selector: 'app-companies-list',
  templateUrl: './companies-list.component.html',
  styleUrls: ['./companies-list.component.css'],
})
export class CompaniesListComponent implements OnInit {
  companies: Array<any> = [];
  displayedColumns: string[] = ['number', 'name', 'symbol','value', 'growing', 'growing_by', 'details'];
  dataSource = new MatTableDataSource(this.companies);

  @ViewChild(MatPaginator) paginator?: MatPaginator;

  constructor(
    private stockDataService: StockDataService,
    private router: Router
  ) {
    this.stockDataService.getCompaniesList().subscribe((response) => {
      console.log(response)
      this.companies = response.companies;
      this.dataSource.data = this.companies;
    });
  }
  ngOnInit(): void {}

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator!;
  }

  openCompanyPage(companyName: any) {
    // this.router.navigate(['/' + companyName]);
    this.router.navigate(['/company/' + companyName]);
  }

}
