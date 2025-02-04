package com.quickcrams.quickcrams.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import com.quickcrams.quickcrams.models.Flashcard;

public interface FlashcardRepository extends JpaRepository<Flashcard, Long> {
}