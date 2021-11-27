import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { StockDataService } from '../services/stock-data.service';

@Component({
  selector: 'app-new-data',
  templateUrl: './new-data.component.html',
  styleUrls: ['./new-data.component.css'],
})
export class NewDataComponent implements OnInit {
  firstFormGroup!: FormGroup;
  secondFormGroup!: FormGroup;
  fileName: string = '';

  constructor(
    private stockDataService: StockDataService,
    private _formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required],
    });
    this.secondFormGroup = this._formBuilder.group({
      secondCtrl: ['', Validators.required],
    });
  }

  csvInputChange(fileInputEvent: any) {
    // console.log(fileInputEvent.target.files[0]);
    this.stockDataService
      .postFileWithData(fileInputEvent.target.files[0])
      .subscribe((response) => {
        this.fileName = fileInputEvent.target.files[0].name;
      });
  }
}
