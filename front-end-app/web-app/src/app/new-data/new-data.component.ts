import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { StockDataService } from '../services/stock-data.service';

export interface Model {
  value: number;
  viewValue: string;
}
@Component({
  selector: 'app-new-data',
  templateUrl: './new-data.component.html',
  styleUrls: ['./new-data.component.css'],
})
export class NewDataComponent implements OnInit {
  firstFormGroup!: FormGroup;

  fileName: string = '';
  file?: File;
  models: Array<Model> = [];
  selectedModelID: number = 0;

  constructor(
    private stockDataService: StockDataService,
    private _formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required],
    });

    this.stockDataService.getModels().subscribe((response) => {
      this.models = this.reformatModels(response);
      console.log(this.models);
    });
  }

  csvInputChange(fileInputEvent: any) {
    this.file = fileInputEvent.target.files[0];
    this.fileName = fileInputEvent.target.files[0].name;
    // console.log(fileInputEvent.target.files[0]);
    // this.stockDataService
    //   .postFileWithData(fileInputEvent.target.files[0])
    //   .subscribe((response) => {
    //     this.fileName = fileInputEvent.target.files[0].name;
    //   });
  }

  sendDataToBackend() {
    console.log(this.file, this.selectedModelID);

    this.stockDataService
      .postFileWithData(this.file, this.selectedModelID)
      .subscribe((response) => {
        console.log(response);
      });
  }

  reformatModels(models: Array<any>) {
    let returnArray: Array<Model> = [];
    models.forEach((m: any) => {
      returnArray.push({ value: m.id, viewValue: m.name });
    });
    return returnArray;
  }
}
