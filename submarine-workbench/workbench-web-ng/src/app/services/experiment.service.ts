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

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ListResult, Rest } from '@submarine/interfaces';
import { ExperimentInfo } from '@submarine/interfaces/experiment-info';
import { BaseApiService } from '@submarine/services/base-api.service';
import { of, Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ExperimentService {
  constructor(private baseApi: BaseApiService, private httpClient: HttpClient) {
  }

  fetchExperimentList(): Observable<ExperimentInfo[]> {
    const apiUrl = this.baseApi.getRestApi('/v1/jobs');
    return this.httpClient.get<Rest<any>>(apiUrl).pipe(
      switchMap(res => {
        // TODO(pingsutw): res.success should not return NULL
        // @ts-ignore
        if (res.status === 'OK') {
          console.log(res.result);
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'get');
        }
      })
    );
  }
}
