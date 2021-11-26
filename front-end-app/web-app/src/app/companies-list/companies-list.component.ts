import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  Input,
} from '@angular/core';
import { StockDataService } from '../services/stock-data.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { MatSort } from '@angular/material/sort';

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
  displayedColumns: string[] = [
    'number',
    'name',
    'symbol',
    'value',
    'growing',
    'growing_by',
    'details',
  ];
  dataSource = new MatTableDataSource(this.companies);

  @ViewChild(MatPaginator) paginator?: MatPaginator;
  @ViewChild(MatSort) sort?: MatSort;

  constructor(
    private stockDataService: StockDataService,
    private router: Router
  ) {}
  ngOnInit(): void {
    this.getData();
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator!;
    this.dataSource.sort = this.sort!;
  }

  openCompanyPage(companyName: any) {
    // this.router.navigate(['/' + companyName]);
    this.router.navigate(['/company/' + companyName]);
  }

  async openAdditionForm() {
    var user_input;
    user_input = prompt('Symbol spółki', 'Tu wpisz symbol spółki');
    if (user_input != null) {
      this.stockDataService.addNewCompany(user_input).subscribe((response) => {
        console.log(response);
      });

      await this.delay(3000);
      window.location.reload();
    }
  }

  delay(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  getData() {
    this.stockDataService.getCompaniesList().subscribe((response) => {
      this.companies = response.companies;
      this.dataSource.data = this.companies;
    });
  }
}
