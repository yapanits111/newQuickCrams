package com.quickcrams.quickcrams.repositories;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.quickcrams.quickcrams.models.User;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}