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

package org.apache.submarine.server.rest;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import org.apache.submarine.server.SubmarineServer;
import org.apache.submarine.server.api.experiment.Experiment;
import org.apache.submarine.server.api.experiment.ExperimentId;
import org.apache.submarine.server.api.spec.EnvironmentSpec;
import org.apache.submarine.server.api.spec.ExperimentSpec;
import org.apache.submarine.server.experiment.ExperimentManager;
import org.apache.submarine.server.response.JsonResponse;
import org.junit.Before;
import org.junit.BeforeClass;

import javax.ws.rs.core.Response;
import java.lang.reflect.Type;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;


public class ExperimentRestApiTest {
  private static ExperimentRestApi experimentRestApi;
  private static ExperimentManager mockExperimentManager;
  private final AtomicInteger experimentCounter = new AtomicInteger(0);

  private static GsonBuilder gsonBuilder = new GsonBuilder();
  private static Gson gson = gsonBuilder.setDateFormat("yyyy-MM-dd HH:mm:ss").create();

  @BeforeClass
  public static void init() {
    mockExperimentManager = mock(ExperimentManager.class);
    experimentRestApi = new ExperimentRestApi();
    experimentRestApi.setExperimentManager(mock(ExperimentManager.class));
  }

  @Before
  public void createAndUpdateExperiment() {
    Experiment experiment = new Experiment();
    experiment.setAcceptedTime("2020-08-06T08:39:22.000+08:00");
    experiment.setCreatedTime("2020-08-06T08:39:22.000+08:00");
    experiment.setRunningTime("2020-08-06T08:39:23.000+08:00");
    experiment.setFinishedTime("2020-08-06T08:41:07.000+08:00");
    experiment.setUid("0b617cea-81fa-40b6-bbff-da3e400d2be4");
    experiment.setName("tf-example");
    experiment.setStatus("Succeeded");
    experiment.setExperimentId(ExperimentId.newInstance(SubmarineServer.getServerTimeStamp(),
            experimentCounter.incrementAndGet()));
    ExperimentSpec experimentSpec = new ExperimentSpec();
    EnvironmentSpec environmentSpec = new EnvironmentSpec();
    environmentSpec.setName("foo");
    experimentSpec.setEnvironment(environmentSpec);
    // experimentSpec.setMeta(...);
    // experimentSpec.setSpec(...);
    experiment.setSpec(experimentSpec);

    when(mockExperimentManager.createExperiment(any(ExperimentSpec.class))).thenReturn(experiment);
    Response createExperimentResponse = experimentRestApi.createExperiment(experimentSpec);
    assertEquals(Response.Status.OK.getStatusCode(), createExperimentResponse.getStatus());

    Experiment result = getExperimentFromResponse(createExperimentResponse);
    assertEquals(experiment.getAcceptedTime(), result.getAcceptedTime());
  }

  private Experiment getExperimentFromResponse(Response response) {
    String entity = (String) response.getEntity();
    Type type = new TypeToken<JsonResponse<Experiment>>() {}.getType();
    JsonResponse<Experiment> jsonResponse = gson.fromJson(entity, type);
    return jsonResponse.getResult();
  }
}
