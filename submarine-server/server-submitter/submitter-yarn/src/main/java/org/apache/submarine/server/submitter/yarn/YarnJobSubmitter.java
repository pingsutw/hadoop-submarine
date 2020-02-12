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

package org.apache.submarine.server.submitter.yarn;

import com.linkedin.tony.Constants;
import com.linkedin.tony.TonyClient;
import com.linkedin.tony.client.CallbackHandler;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.yarn.api.records.ApplicationId;
import org.apache.hadoop.yarn.exceptions.YarnException;
import org.apache.submarine.client.cli.param.runjob.RunJobParameters;
import org.apache.submarine.commons.runtime.exception.SubmarineException;
import org.apache.submarine.commons.runtime.param.Parameter;
import org.apache.submarine.commons.runtime.JobSubmitter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

/**
 * Implementation of JobSubmitter with TonY runtime.
 */
public class YarnJobSubmitter implements JobSubmitter, CallbackHandler {

  private static final Log LOG = LogFactory.getLog(YarnJobSubmitter.class);
  private ApplicationId applicationId;
  private TonyClient tonyClient;

  public YarnJobSubmitter() { }
  public void setTonyClient(TonyClient client) {
    this.tonyClient = client;
  }

  @Override
  public ApplicationId submitJob(Parameter parameters)
          throws IOException, SubmarineException {
    LOG.info("Starting Tony runtime..");
    LOG.info("Use ML framework : " + parameters.getFramework().getValue());

    File tonyFinalConfPath = File.createTempFile("temp",
        Constants.TONY_FINAL_XML);
    // Write user's overridden conf to an xml to be localized.
    Configuration tonyConf = null;
    try {
      tonyConf = YarnUtils.tonyConfFromClientContext((RunJobParameters) parameters.getParameters(),
                parameters.getFramework());
    } catch (Exception e) {
      throw new SubmarineException("Failed to create tony conf from client context");
    }
    try (OutputStream os = new FileOutputStream(tonyFinalConfPath)) {
      tonyConf.writeXml(os);
    } catch (IOException e) {
      throw new RuntimeException("Failed to create " + tonyFinalConfPath
          + " conf file. Exiting.", e);
    }

    try {
      tonyClient.init(new String[]{
          "--conf_file", tonyFinalConfPath.getAbsolutePath()
      });
    } catch (Exception e) {
      LOG.error("Failed to init TonyClient: ", e);
    }
    Thread clientThread = new Thread(tonyClient::start);
    java.lang.Runtime.getRuntime().addShutdownHook(new Thread(() -> {
      try {
        tonyClient.forceKillApplication();
      } catch (YarnException | IOException e) {
        LOG.error("Failed to kill application during shutdown.", e);
      }
    }));
    clientThread.start();
    while (clientThread.isAlive()) {
      if (applicationId != null) {
        LOG.info("TonyClient returned applicationId: " + applicationId);
        return applicationId;
      }
      try {
        Thread.sleep(5000);
      } catch (InterruptedException e) {
        LOG.error(e);
      }
    }
    return null;
  }

  @Override
  public void onApplicationIdReceived(ApplicationId appId) {
    applicationId = appId;
  }
}
