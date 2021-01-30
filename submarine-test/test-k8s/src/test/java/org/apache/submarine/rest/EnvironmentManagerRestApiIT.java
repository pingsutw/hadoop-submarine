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

package org.apache.submarine.rest;

import java.io.IOException;

import javax.ws.rs.core.Response;

import org.apache.commons.httpclient.methods.DeleteMethod;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.submarine.server.AbstractSubmarineServerTest;
import org.apache.submarine.server.api.environment.Environment;
import org.apache.submarine.server.api.environment.EnvironmentId;
import org.apache.submarine.server.gson.EnvironmentIdDeserializer;
import org.apache.submarine.server.gson.EnvironmentIdSerializer;
import org.apache.submarine.server.response.JsonResponse;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.After;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

@SuppressWarnings("rawtypes")
public class EnvironmentManagerRestApiIT extends AbstractSubmarineServerTest {
  private final Gson gson = new GsonBuilder()
          .registerTypeAdapter(EnvironmentId.class, new EnvironmentIdSerializer())
          .registerTypeAdapter(EnvironmentId.class, new EnvironmentIdDeserializer())
          .create();

  @BeforeClass
  public static void startUp() throws Exception {
    Assert.assertTrue(checkIfServerIsRunning());
  }

  @Before
  public void testCreateEnvironment() throws Exception {
    LOG.info("Test create Environment using Environment REST API");

    String body = loadContent("environment/test_env_1.json");
    PostMethod postMethod = httpPost(ENV_PATH, body, "application/json");

    JsonResponse jsonResponse = getJsonResponse(postMethod, gson);
    Environment env =
            gson.fromJson(gson.toJson(jsonResponse.getResult()), Environment.class);
    Assert.assertNotNull(env.getEnvironmentSpec().getName());
    Assert.assertNotNull(env.getEnvironmentSpec());
  }

  @Test
  public void testGetEnvironment() throws Exception {
    LOG.info("Test get Environment using Environment REST API");

    GetMethod getMethod = httpGet(ENV_PATH + "/" + ENV_NAME);
    JsonResponse jsonResponse = getJsonResponse(getMethod, gson);

    Environment getEnvironment =
        gson.fromJson(gson.toJson(jsonResponse.getResult()), Environment.class);
    Assert.assertEquals(ENV_NAME, getEnvironment.getEnvironmentSpec().getName());
  }


  @Test
  public void testUpdateEnvironment() throws Exception {
    LOG.info("Test update Environment using Environment REST API");

    String body = loadContent("environment/test_env_2.json");
    String json = httpPatch(ENV_PATH + "/" + ENV_NAME, body, "application/json");

    JsonResponse jsonResponse = gson.fromJson(json, JsonResponse.class);
    Assert.assertEquals(Response.Status.OK.getStatusCode(),
            jsonResponse.getCode());

    Environment env =
            gson.fromJson(gson.toJson(jsonResponse.getResult()), Environment.class);
    Assert.assertEquals(env.getEnvironmentSpec().getDockerImage(),
            "continuumio/miniconda3");
    Assert.assertEquals(1, env.getEnvironmentSpec().getKernelSpec().getDependencies().size());
  }

  @Test
  public void testListEnvironments() throws IOException {
    LOG.info("Test list Environment using Environment REST API");
    GetMethod getMethod = httpGet(ENV_PATH);
    JsonResponse jsonResponse = getJsonResponse(getMethod, gson);

    Environment[] getEnvironment =
            gson.fromJson(gson.toJson(jsonResponse.getResult()), Environment[].class);
    Assert.assertEquals(ENV_NAME, getEnvironment[0].getEnvironmentSpec().getName());
  }

  @After
  public void testDeleteEnvironment() throws Exception {
    LOG.info("Test delete Environment using Environment REST API");

    DeleteMethod deleteMethod = httpDelete(ENV_PATH + "/" + ENV_NAME);
    JsonResponse jsonResponse = getJsonResponse(deleteMethod, gson);

    Environment deletedEnv =
            gson.fromJson(gson.toJson(jsonResponse.getResult()), Environment.class);
    Assert.assertEquals(ENV_NAME, deletedEnv.getEnvironmentSpec().getName());

    GetMethod getMethod = httpGet(ENV_PATH + "/" + ENV_NAME);
    Assert.assertEquals(Response.Status.NOT_FOUND.getStatusCode(),
        getMethod.getStatusCode());
  }
}
