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
import { Rest } from '@submarine/interfaces';
import { ExperimentInfo } from '@submarine/interfaces/experiment-info';
import { BaseApiService } from '@submarine/services/base-api.service';
import { of, throwError, Observable } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ExperimentService {
  constructor(private baseApi: BaseApiService, private httpClient: HttpClient) {}

  fetchExperimentList(): Observable<ExperimentInfo[]> {
    const apiUrl = this.baseApi.getRestApi('/v1/experiment');
    return this.httpClient.get<Rest<ExperimentInfo[]>>(apiUrl).pipe(
      switchMap((res) => {
        if (res.success) {
          console.log(res.result);
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'get');
        }
      })
    );
  }

  querySpecificExperiment(id: string): Observable<ExperimentInfo> {
    const apiUrl = this.baseApi.getRestApi('/v1/experiment/' + id);
    return this.httpClient.get<Rest<ExperimentInfo>>(apiUrl).pipe(
      switchMap((res) => {
        if (res.success) {
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'get');
        }
      })
    );
  }

  createExperiment(experimentSpec): Observable<ExperimentInfo> {
    const apiUrl = this.baseApi.getRestApi('/v1/experiment');
    return this.httpClient.post<Rest<ExperimentInfo>>(apiUrl, experimentSpec).pipe(
      map((res) => res.result), // return result directly if succeeding
      catchError((e) => {
        let message: string;
        if (e.error instanceof ErrorEvent) {
          // client side error
          message = 'Something went wrong with network or workbench';
        } else {
          console.log(e);
          if (e.status === 409) {
            message = 'You might have a duplicate experiment name';
          } else if (e.status >= 500) {
            message = `${e.message}`;
          } else {
            message = e.error.message;
          }
        }
        return throwError(message);
      })
    );
  }

  editExperiment(experimentSpec): Observable<ExperimentInfo> {
    const apiUrl = this.baseApi.getRestApi('/v1/experiment');
    return this.httpClient.patch<Rest<ExperimentInfo>>(apiUrl, experimentSpec).pipe(
      switchMap((res) => {
        if (res.success) {
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'patch', experimentSpec);
        }
      })
    );
  }

  deleteExperiment(id: string): Observable<ExperimentInfo> {
    const apiUrl = this.baseApi.getRestApi('/v1/experiment/' + id);
    return this.httpClient.delete<Rest<any>>(apiUrl).pipe(
      switchMap((res) => {
        if (res.success) {
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'delete', id);
        }
      })
    );
  }

  getExperimentLog(id: string): Observable<any> {
    const apiUrl = this.baseApi.getRestApi('/v1/experiment/logs/' + id);
    return this.httpClient.get<Rest<any>>(apiUrl).pipe(
      switchMap((res) => {
        if (res.success) {
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'get', id);
        }
      })
    );
  }

  getExperimentParam(param: object): Observable<any> {
    const apiUrl = this.baseApi.getRestApi('/param/selective');
    return this.httpClient.post<any>(apiUrl, param).pipe(
      switchMap((res) => {
        if (res.success) {
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'post', param);
        }
      })
    );
  }

  getExperimentMetric(param: object): Observable<any> {
    const apiUrl = this.baseApi.getRestApi('/metric/selective');
    return this.httpClient.post<any>(apiUrl, param).pipe(
      switchMap((res) => {
        if (res.success) {
          return of(res.result);
        } else {
          throw this.baseApi.createRequestError(res.message, res.code, apiUrl, 'post', param);
        }
      })
    );
  }

  durationHandle(secs: number) {
    const hr = Math.floor(secs / 3600);
    const min = Math.floor((secs - hr * 3600) / 60);
    const sec = Math.round(secs) - hr * 3600 - min * 60;
    let showHr;
    let showMin;
    let showSec;
    if (hr < 10) {
      showHr = '0' + hr;
    } else {
      showHr = hr.toString();
    }
    if (min < 10) {
      showMin = '0' + min;
    } else {
      showMin = min.toString();
    }
    if (sec < 10) {
      showSec = '0' + sec;
    } else {
      showSec = sec.toString();
    }
    return showHr + ':' + showMin + ':' + showSec;
  }
}
