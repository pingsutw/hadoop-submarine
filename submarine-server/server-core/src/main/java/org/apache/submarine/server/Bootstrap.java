package org.apache.submarine.server;

import io.swagger.v3.jaxrs2.integration.JaxrsOpenApiContextBuilder;
import io.swagger.v3.oas.integration.SwaggerConfiguration;
import io.swagger.v3.oas.integration.OpenApiConfigurationException;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Bootstrap extends HttpServlet {
  @Override
  public void init(ServletConfig config) throws ServletException {

    OpenAPI oas = new OpenAPI();
    Info info = new Info()
             .title("Submarine Experiment API")
             .description("The Submarine REST API allows you to create, list, and get experiments. The" +
                     "API is hosted under the /v1/jobs route on the Submarine server. For example," +
                     "to list experiments on a server hosted at http://localhost:8080, access" +
                     "http://localhost:8080/api/v1/jobs/")
             .termsOfService("http://swagger.io/terms/")
             .contact(new Contact()
             .email("submarine-dev@submarine.apache.org"))
             .version("0.4.0-SNAPSHOT")
             .license(new License()
             .name("Apache 2.0")
             .url("http://www.apache.org/licenses/LICENSE-2.0.html"));

    oas.info(info);
    List<Server> servers = new ArrayList<>();
    servers.add(new Server().url("/api"));
    oas.servers(servers);
    SwaggerConfiguration oasConfig = new SwaggerConfiguration()
            .openAPI(oas)
            .resourcePackages(Stream.of("org.apache.submarine.server.rest").collect(Collectors.toSet()));

    try {
      new JaxrsOpenApiContextBuilder()
              .servletConfig(config)
              .openApiConfiguration(oasConfig)
              .buildContext(true);
    } catch (OpenApiConfigurationException e) {
      throw new ServletException(e.getMessage(), e);
    }
  }
}

