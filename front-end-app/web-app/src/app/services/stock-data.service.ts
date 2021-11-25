import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { HistoricalData } from '../model';

@Injectable({
  providedIn: 'root',
})
export class StockDataService {
  baseURL: string = 'http://localhost:5000/flask';

  public historicalData: Subject<HistoricalData[]> = new Subject();

  constructor(private http: HttpClient) {}

  getData(): Observable<any> {
    return this.http.get(this.baseURL, {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  getCompaniesList(): Observable<any> {
    return this.http.get(this.baseURL + '/list/companies', {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  getCompanyData(name: string): Observable<any> {
    return this.http.get(this.baseURL + '/data/' + name, {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  getPopularCompanies(): Observable<any> {
    return this.http.get(this.baseURL + '/popular' , {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }
}
