package com.quickcrams.quickcrams.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.quickcrams.quickcrams.models.Flashcard;
import com.quickcrams.quickcrams.repositories.FlashcardRepository;

@RestController
@RequestMapping("/api/flashcards")
public class FlashcardsController {

    @Autowired
    private FlashcardRepository flashcardRepository;

    @PostMapping
    public ResponseEntity<String> createFlashcard(@RequestBody Flashcard flashcard) {
        flashcardRepository.save(flashcard); // Save flashcard to the database
        return ResponseEntity.ok("Flashcard created");
    }

    @GetMapping
    public ResponseEntity<List<Flashcard>> getFlashcards() {
        List<Flashcard> flashcards = flashcardRepository.findAll(); // Retrieve flashcards
        return ResponseEntity.ok(flashcards);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteFlashcard(@PathVariable Long id) {
        flashcardRepository.deleteById(id); // Delete flashcard by ID
        return ResponseEntity.ok("Flashcard deleted");
    }
}