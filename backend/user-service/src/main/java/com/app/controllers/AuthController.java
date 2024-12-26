package com.app.controllers;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import com.app.config.JwtUtils;
import com.app.entities.Role;
import com.app.entities.User;
import com.app.repositories.RoleRepository;

import com.app.services.AuthenService;

import java.util.HashSet;
import java.util.Map;

import java.util.Set;

@RestController
@RequestMapping("/auth")
public class AuthController {

	@Autowired
	private AuthenService userService;

	@Autowired
	private PasswordEncoder passwordEncoder;

	@Autowired
	private RoleRepository roleRepository;

	@Autowired
	private JwtUtils jwtUtils;

	@PostMapping("/register")
	public ResponseEntity<?> register(@RequestBody User user) {
		try {

			user.setPassword(passwordEncoder.encode(user.getPassword()));

			if (user.getRoles() == null || user.getRoles().isEmpty()) {
				throw new IllegalArgumentException("At least one role is required for registration.");
			}

			Set<Role> roleSet = new HashSet<>();
			for (Role role : user.getRoles()) {
				if (role.getName() == null || role.getName().isEmpty()) {
					return ResponseEntity.badRequest().body("Role name cannot be null or empty.");
				}
				Role existingRole = roleRepository.findByName(role.getName());
				if (existingRole == null) {
					existingRole = roleRepository.save(new Role(role.getName()));
				}
				roleSet.add(existingRole);
			}
			user.setRoles(roleSet);

			userService.saveUser(user);
			return ResponseEntity.ok("User registered successfully!");
		} catch (IllegalArgumentException e) {
			return ResponseEntity.badRequest().body(e.getMessage());
		} catch (Exception e) {
			return ResponseEntity.internalServerError()
					.body("An error occurred during registration: " + e.getMessage());
		}
	}

	@PostMapping("/login")
	public ResponseEntity<?> login(@RequestBody Map<String, String> request) {
		try {
			String username = request.get("username");
			String password = request.get("password");

			if (username == null || username.isEmpty()) {
				return ResponseEntity.badRequest().body("Username cannot be null or empty.");
			}
			if (password == null || password.isEmpty()) {
				return ResponseEntity.badRequest().body("Password cannot be null or empty.");
			}

			User user = userService.findByUsername(username);
			if (user == null) {
				return ResponseEntity.status(404).body("User not found.");
			}
			if (passwordEncoder.matches(password, user.getPassword())) {
				String token = jwtUtils.generateToken(username, user.getRoles());
				return ResponseEntity.ok(Map.of("token", token, "roles", user.getRoles()));
			} else {
				return ResponseEntity.status(401).body("Invalid credentials.");
			}
		} catch (Exception e) {
			return ResponseEntity.internalServerError().body("An error occurred during login: " + e.getMessage());
		}
	}
}
