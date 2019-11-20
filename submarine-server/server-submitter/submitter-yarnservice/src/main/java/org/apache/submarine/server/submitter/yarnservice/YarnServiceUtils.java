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

package org.apache.submarine.server.submitter.yarnservice;

import com.google.common.annotations.VisibleForTesting;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.yarn.client.api.AppAdminClient;

import static org.apache.hadoop.yarn.client.api.AppAdminClient.DEFAULT_TYPE;

/**
 * This class contains some static helper methods to query DNS data
 * based on the provided parameters.
 */
public final class YarnServiceUtils {
  private static AppAdminClientFactory appAdminClientFactory =
      new AppAdminClientFactory();

  private YarnServiceUtils() {
  }

  @VisibleForTesting
  public static void setAppAdminClientFactory(
      AppAdminClientFactory appAdminClientFactory) {
    YarnServiceUtils.appAdminClientFactory = appAdminClientFactory;
  }

  static AppAdminClient createServiceClient(
      Configuration yarnConfiguration) {
    return appAdminClientFactory.createDefault(yarnConfiguration);
  }

  public static String getDNSName(String serviceName,
      String componentInstanceName, String userName, String domain, int port) {
    return componentInstanceName + getDNSNameCommonSuffix(serviceName, userName,
        domain, port);
  }

  public static String getDNSNameCommonSuffix(String serviceName,
      String userName, String domain, int port) {
    return "." + serviceName + "." + userName + "." + domain + ":" + port;
  }

  public static class AppAdminClientFactory {
    public AppAdminClient createDefault(Configuration configuration) {
      return AppAdminClient.createAppAdminClient(DEFAULT_TYPE, configuration);
    }
  }
}
