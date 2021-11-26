import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSortModule } from '@angular/material/sort';
import { ChartViewerComponent } from './chart-viewer/chart-viewer.component';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { HttpClientModule } from '@angular/common/http';
import { CompaniesListComponent } from './companies-list/companies-list.component';
import { MatTableModule } from '@angular/material/table';
import { Routes, RouterModule } from '@angular/router';
import { CompanyComponent } from './company/company.component';
import { HomeComponent } from './home/home.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { NewDataComponent } from './new-data/new-data.component';
import { MatGridListModule } from '@angular/material/grid-list';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'list', component: CompaniesListComponent },
  { path: 'new-data', component: NewDataComponent },
  { path: 'company/:id', component: CompanyComponent },
];
@NgModule({
  declarations: [
    AppComponent,
    ChartViewerComponent,
    CompaniesListComponent,
    CompanyComponent,
    HomeComponent,
    NewDataComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatSortModule,
    MatIconModule,
    NgxChartsModule,
    HttpClientModule,
    MatTableModule,
    MatGridListModule,
    MatPaginatorModule,
    RouterModule.forRoot(routes),
  ],
  providers: [],
  bootstrap: [AppComponent],
  exports: [RouterModule],
})
export class AppModule {}
