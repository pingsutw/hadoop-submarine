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

import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.PATCH;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.List;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;

import org.apache.submarine.commons.utils.exception.SubmarineRuntimeException;
import org.apache.submarine.server.job.JobManager;
import org.apache.submarine.server.api.job.Job;
import org.apache.submarine.server.api.spec.JobSpec;
import org.apache.submarine.server.response.JsonResponse;

/**
 * Job Service REST API v1. It can accept {@link JobSpec} to create a job.
 */
@Path(RestConstants.V1 + "/" + RestConstants.JOBS)
@Produces({MediaType.APPLICATION_JSON + "; " + RestConstants.CHARSET_UTF8})
public class JobManagerRestApi {
  private final JobManager jobManager = JobManager.getInstance();
  /**
   * Return the Pong message for test the connectivity
   * @return Pong message
   */
  @GET
  @Path(RestConstants.PING)
  @Consumes(MediaType.APPLICATION_JSON)
  @Operation(summary = "Ping submarine server",
          tags = {"jobs"},
          description = "Return the Pong message for test the connectivity",
          responses = {
                  @ApiResponse(responseCode = "200", description = "successful operation")})
  public Response ping() {
    return new JsonResponse.Builder<String>(Response.Status.OK)
        .success(true).result("Pong").build();
  }

  /**
   * Returns the contents of {@link Job} that submitted by user.
   * @param spec job spec
   * @return the contents of job
   */
  @POST
  @Consumes({RestConstants.MEDIA_TYPE_YAML, MediaType.APPLICATION_JSON})
  @Operation(summary = "Create a job",
          tags = {"jobs"},
          responses = {
                  @ApiResponse(description = "successful operation", content = @Content(
                          schema = @Schema(implementation = Job.class)))})
  public Response createJob(JobSpec spec) {
    try {
      Job job = jobManager.createJob(spec);
      return new JsonResponse.Builder<Job>(Response.Status.OK).result(job).build();
    } catch (SubmarineRuntimeException e) {
      return parseJobServiceException(e);
    }
  }

  /**
   * List all job for the user
   * @return job list
   */
  @GET
  @Operation(summary = "List jobs",
          tags = {"jobs"},
          responses = {
                  @ApiResponse(description = "successful operation", content = @Content(
                          schema = @Schema(implementation = Job.class)))})
  public Response listJob(@QueryParam("status") String status) {
    try {
      List<Job> jobList = jobManager.listJobsByStatus(status);
      return new JsonResponse.Builder<List<Job>>(Response.Status.OK).result(jobList).build();
    } catch (SubmarineRuntimeException e) {
      return parseJobServiceException(e);
    }
  }

  /**
   * Returns the job detailed info by specified job id
   * @param id job id
   * @return the detailed info of job
   */
  @GET
  @Path("/{id}")
  @Operation(summary = "Find job by id",
          tags = {"jobs"},
          responses = {
                  @ApiResponse(description = "successful operation", content = @Content(
                          schema = @Schema(implementation = Job.class))),
                  @ApiResponse(responseCode = "404", description = "Job not found")})
  public Response getJob(@PathParam(RestConstants.JOB_ID) String id) {
    try {
      Job job = jobManager.getJob(id);
      return new JsonResponse.Builder<Job>(Response.Status.OK).result(job).build();
    } catch (SubmarineRuntimeException e) {
      return parseJobServiceException(e);
    }
  }

  @PATCH
  @Path("/{id}")
  @Consumes({RestConstants.MEDIA_TYPE_YAML, MediaType.APPLICATION_JSON})
  @Operation(summary = "Update the job in the submarine server with job spec",
          tags = {"jobs"},
          responses = {
                  @ApiResponse(description = "successful operation", content = @Content(
                          schema = @Schema(implementation = Job.class))),
                  @ApiResponse(responseCode = "404", description = "Job not found")})
  public Response patchJob(@PathParam(RestConstants.JOB_ID) String id, JobSpec spec) {
    try {
      Job job = jobManager.patchJob(id, spec);
      return new JsonResponse.Builder<Job>(Response.Status.OK).success(true)
          .result(job).build();
    } catch (SubmarineRuntimeException e) {
      return parseJobServiceException(e);
    }
  }

  /**
   * Returns the job that deleted
   * @param id job id
   * @return the detailed info about deleted job
   */
  @DELETE
  @Path("/{id}")
  @Operation(summary = "Delete the job",
          tags = {"jobs"},
          responses = {
                  @ApiResponse(description = "successful operation", content = @Content(
                          schema = @Schema(implementation = Job.class))),
                  @ApiResponse(responseCode = "404", description = "Job not found")})
  public Response deleteJob(@PathParam(RestConstants.JOB_ID) String id) {
    try {
      Job job = jobManager.deleteJob(id);
      return new JsonResponse.Builder<Job>(Response.Status.OK)
          .result(job).build();
    } catch (SubmarineRuntimeException e) {
      return parseJobServiceException(e);
    }
  }

  private Response parseJobServiceException(SubmarineRuntimeException e) {
    return new JsonResponse.Builder<String>(e.getCode()).message(e.getMessage()).build();
  }
}
