package com.quickcrams.quickcrams.repositories;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.quickcrams.quickcrams.models.UserRoles;

public interface UserRolesRepository extends JpaRepository<UserRoles, Long> {

    List<UserRoles> findByUserId(Long userId);

    List<UserRoles> findByRoleId(Long roleId);
}
