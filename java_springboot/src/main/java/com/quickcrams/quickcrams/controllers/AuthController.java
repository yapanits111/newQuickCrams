package com.quickcrams.quickcrams.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.quickcrams.quickcrams.models.User;
import com.quickcrams.quickcrams.repositories.UserRepository;
import com.quickcrams.quickcrams.security.JwtUtils;

@RestController
@RequestMapping("/api")
public class AuthController {

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtils jwtUtils;

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/register")
    public ResponseEntity<String> registerUser (@RequestBody User user) {
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        userRepository.save(user); // Save user to the database
        return ResponseEntity.ok("User  registered successfully!");
    }

    @PostMapping("/login")
    public ResponseEntity<String> loginUser (@RequestBody User user) {
        String token = jwtUtils.generateToken(user.getUsername());
        return ResponseEntity.ok("JWT Token: " + token);
    }
}