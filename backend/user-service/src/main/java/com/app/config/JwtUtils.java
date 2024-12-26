package com.app.config;

import io.jsonwebtoken.SignatureAlgorithm;

import org.springframework.stereotype.Component;

import com.app.entities.Role;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Date;
import java.util.Set;
import java.util.stream.Collectors;

@Component
public class JwtUtils {

	private static final String SECRET_KEY = "your-secure-long-secret-key-32-characters-or-more";
    private static final Key SIGNING_KEY = Keys.hmacShaKeyFor(SECRET_KEY.getBytes(StandardCharsets.UTF_8));

    
    public String generateToken(String username, Set<Role> roles) {
 
        Set<String> roleNames = roles.stream()
                .map(Role::getName) 
                .collect(Collectors.toSet());

        long expirationTime = 1000 * 60 * 60 * 24; // Durée de validité  1 jour

        return Jwts.builder()
                .setSubject(username) 
                .claim("roles", roleNames) 
                .setIssuedAt(new Date()) 
                .setExpiration(new Date(System.currentTimeMillis() + expirationTime)) 
                .signWith(SIGNING_KEY, SignatureAlgorithm.HS256) 
                .compact();
    }



    
    public Claims validateToken(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(SIGNING_KEY) 
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}
