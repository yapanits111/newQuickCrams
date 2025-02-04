package com.quickcrams.quickcrams.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import com.quickcrams.quickcrams.models.Note;

public interface NoteRepository extends JpaRepository<Note, Long> {
}