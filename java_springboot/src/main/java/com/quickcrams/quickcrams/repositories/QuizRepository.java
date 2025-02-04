package com.quickcrams.quickcrams.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import com.quickcrams.quickcrams.models.Quiz;

public interface QuizRepository extends JpaRepository<Quiz, Long> {
}