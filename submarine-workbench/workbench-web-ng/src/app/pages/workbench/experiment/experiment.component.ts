/*!
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ExperimentInfo } from '@submarine/interfaces/experiment-info';
import { ExperimentService } from '@submarine/services/experiment.service';
import { NzMessageService } from 'ng-zorro-antd';

@Component({
  selector: 'submarine-job',
  templateUrl: './experiment.component.html',
  styleUrls: ['./experiment.component.scss']
})
export class ExperimentComponent implements OnInit {

  experimentList: ExperimentInfo[] = [];
  // About show existing experiments
  showJob = 'All';
  searchText = '';

  // About new experiment
  createJob: FormGroup;
  current = 0;
  okText = 'Next Step';
  isVisible = false;

  ExperimentSpecs = ['Adhoc', 'Predefined'];
  ruleTemplates = ['Template1', 'Template2'];
  ruleTypes = ['Strong', 'Weak'];
  scheduleCycles = ['Month', 'Week'];

  constructor(
    private experimentService: ExperimentService,
    private nzMessageService: NzMessageService
  ) { }

  ngOnInit() {
    this.createJob =  new FormGroup({
      'jobName': new FormControl(null, Validators.required),
      'description': new FormControl(null, [Validators.required]),
      'experimentSpec': new FormControl('Adhoc'),
      'ruleTemplate': new FormControl('Template1'),
      'ruleType': new FormControl('Strong'),
      'startDate': new FormControl(new Date()),
      'scheduleCycle': new FormControl('Month')
    });
    this.fetchExperimentList();
  }

  handleOk() {
    if (this.current === 1) {
      this.okText = 'Submit';
      this.current++;
    } else if (this.current === 2) {
      this.okText = 'Next Step';
      this.current = 0;
      this.isVisible = false;
      // TODO(jasoonn): Create Real experiment
      console.log(this.createJob);
    } else {
      this.current++;
    }
  }

  fetchExperimentList() {
    this.experimentService
      .fetchExperimentList()
      .subscribe((  list ) => {
        this.experimentList = list;
      });
  }
  onDeleteExperiment(data: ExperimentInfo) {
    console.log("id", data.jobId);
    this.experimentService.deleteExperiment(data.jobId).subscribe(
      () => {
        console.log("success");
        this.nzMessageService.success('Delete user success!');
        this.fetchExperimentList();
      }, err => {
        console.log("failed");
        this.nzMessageService.success(err.message);
      }
    );
  }

  // TODO(jasoonn): Filter experiment list
  filter(event) {
    console.log(this.searchText + event.key);
  }
  // TODO(jasoonn): Perform part of list
  showChange() {
    console.log("Change to " + this.showJob);
  }
  // TODO(jasoonn): Start experiment
  startJob(job) {
    console.log(job);
  }
  // TODO(jasoonn): Edit experiment
  editJob(job) {
    console.log(job);
  }
}
