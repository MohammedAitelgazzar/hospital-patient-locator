package com.app;

import org.springframework.boot.SpringApplication;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.ReactiveDiscoveryClient;
import org.springframework.cloud.gateway.discovery.DiscoveryClientRouteDefinitionLocator;
import org.springframework.cloud.gateway.discovery.DiscoveryLocatorProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.web.client.RestClient;

@SpringBootApplication

public class GatewayServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(GatewayServerApplication.class, args);
	}

	@Bean
	RestClient.Builder restClientBuilder() {
		return RestClient.builder();
	}

	@Bean
	DiscoveryClientRouteDefinitionLocator routesDynamique(ReactiveDiscoveryClient rdc, DiscoveryLocatorProperties dlp){
		return new DiscoveryClientRouteDefinitionLocator(rdc,dlp);
	}


	@Bean
	RouteLocator routes(RouteLocatorBuilder builder) {
		return builder.routes()
				.route(r -> r.path("/users/**", "/auth/**")
						.uri("lb://USER-SERVICE"))
				.route(r -> r.path("/location/**")
						.uri("http://localhost:5000"))
				.route(r -> r.path("/health/**")
						.uri("lb://HEALTH-DATA-SERVICE"))
				.route(r -> r.path("/notifications/**")
						.uri("lb://NOTIFICATION-SERVICE"))
				.route(r -> r.path("/hallway/**")
						.uri("lb://HALLWAY-DETECTION-SERVICE"))
				.build();
	}
}
