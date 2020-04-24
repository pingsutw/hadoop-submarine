package org.apache.submarine.server;

import io.swagger.jaxrs.config.SwaggerContextService;
import io.swagger.models.Contact;
import io.swagger.models.Info;
import io.swagger.models.License;
import io.swagger.models.Swagger;


import javax.servlet.http.HttpServlet;
import javax.servlet.ServletContext;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;

public class Bootstrap extends HttpServlet {
  @Override
  public void init(ServletConfig config) throws ServletException {
    Info info = new Info()
            .title("Swagger Server")
            .description("The Submarine REST API allows you to create, list, and get experiments." +
                    " The API is hosted under the /v1/jobs route on the Submarine server. For example," +
                    " to list experiments on a server hosted at http://localhost:8080" +
                    ", access http://localhost:8080/api/v1/jobs/status")
            .termsOfService("http://swagger.io/terms/")
            .contact(new Contact()
                    .email("submarine-dev@submarine.apache.org"))
            .license(new License()
                    .name("Apache 2.0")
                    .url("http://www.apache.org/licenses/LICENSE-2.0.html"));

    ServletContext context = config.getServletContext();
    Swagger swagger = new Swagger().info(info);

    new SwaggerContextService().withServletConfig(config).updateSwagger(swagger);
  }
}
