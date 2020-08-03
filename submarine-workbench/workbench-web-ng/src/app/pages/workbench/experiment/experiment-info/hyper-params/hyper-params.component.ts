/*
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

import { Component, Input, OnInit, SimpleChanges } from '@angular/core';

@Component({
  selector: 'submarine-hyper-params',
  templateUrl: './hyper-params.component.html',
  styleUrls: ['./hyper-params.component.scss']
})
export class HyperParamsComponent implements OnInit {
  @Input() workerIndex: string;
  @Input() paramData;
  podParam = [];

  constructor() {}

  ngOnInit() {}

  ngOnChanges(chg: SimpleChanges) {
    this.podParam.length = 0;
    this.paramData.forEach((data) => {
      if (this.workerIndex.indexOf(data.workerIndex) >= 0) {
        this.podParam.push(data);
      }
    });
  }
}
