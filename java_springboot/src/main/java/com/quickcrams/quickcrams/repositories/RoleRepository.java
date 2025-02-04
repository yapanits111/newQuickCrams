package com.quickcrams.quickcrams.repositories;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.quickcrams.quickcrams.models.Role;

public interface RoleRepository extends JpaRepository<Role, Long> {
    Optional<Role> findByName(String name);
}
