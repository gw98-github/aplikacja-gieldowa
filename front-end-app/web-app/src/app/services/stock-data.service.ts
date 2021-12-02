import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { HistoricalData } from '../model';
import { delay } from 'rxjs/operators';

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
    return this.http.get(this.baseURL + '/popular', {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  getCandidatesList(): Observable<any> {
    return this.http.get(this.baseURL + '/candidates', {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  getModels(): Observable<any> {
    return this.http.get(this.baseURL + '/predictors', {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  addNewCompany(name: string): Observable<any> {
    return this.http.get(this.baseURL + '/add_company/' + name, {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  getPrediction(id: number): Observable<any> {
    return this.http.get(this.baseURL + '/own_prediction/' + id, {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }

  postFileWithData(file: any, id: number) {
    let formData = new FormData();

    formData.append('dataFile', file, file.name);
    formData.append('modelId', id.toString());
    return this.http.post(this.baseURL + '/upload_data', formData, {
      headers: { header: 'Access-Control-Allow-Origin' },
    });
  }
}
