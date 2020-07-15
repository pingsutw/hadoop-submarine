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
package org.apache.submarine.server.workbench.rest;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.apache.ibatis.session.SqlSession;
import org.apache.submarine.server.workbench.annotation.SubmarineApi;
import org.apache.submarine.server.workbench.database.entity.SysUser;
import org.apache.submarine.server.workbench.database.mappers.SysUserMapper;
import org.apache.submarine.server.database.utils.MyBatisUtil;
import org.apache.submarine.server.response.JsonResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Inject;
import javax.inject.Singleton;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Response;
import java.util.HashMap;

@Path("/auth")
@Produces("application/json")
@Singleton
public class LoginRestApi {
  private static final Logger LOG = LoggerFactory.getLogger(LoginRestApi.class);
  private static final Gson gson = new Gson();

  @Inject
  public LoginRestApi() {
  }

  @POST
  @Path("/login")
  @SubmarineApi
  public Response login(String loginParams) {
    HashMap<String, String> mapParams
        = gson.fromJson(loginParams, new TypeToken<HashMap<String, String>>() {}.getType());

    SysUser sysUser = null;
    try (SqlSession sqlSession = MyBatisUtil.getSqlSession()) {
      SysUserMapper sysUserMapper = sqlSession.getMapper(SysUserMapper.class);
      sysUser = sysUserMapper.login(mapParams);
      if (sysUser != null) {
        sysUser.setToken("mock_token");
      } else {
        LOG.info("User Not Found. Please try again");
      }
    } catch (Exception e) {
      LOG.error(e.getMessage(), e);
      return new JsonResponse.Builder<>(Response.Status.OK).success(false).build();
    }

    return new JsonResponse.Builder<SysUser>(Response.Status.OK).success(true).result(sysUser).build();
  }

  @POST
  @Path("/2step-code")
  @SubmarineApi
  public Response step() {
    String data = "{stepCode:1}";

    return new JsonResponse.Builder<String>(Response.Status.OK).success(true).result(data).build();
  }

  @POST
  @Path("/logout")
  @SubmarineApi
  public Response logout() {
    return new JsonResponse.Builder<Boolean>(Response.Status.OK).success(true).result(true).build();
  }
}
