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

import com.quickcrams.quickcrams.models.Note;
import com.quickcrams.quickcrams.repositories.NoteRepository;

@RestController
@RequestMapping("/api/notes")
public class NotesController {

    @Autowired
    private NoteRepository noteRepository;

    @PostMapping
    public ResponseEntity<String> createNote(@RequestBody Note note) {
        noteRepository.save(note); // Save note to the database
        return ResponseEntity.ok("Note created");
    }

    @GetMapping
    public ResponseEntity<List<Note>> getNotes() {
        List<Note> notes = noteRepository.findAll(); // Retrieve notes
        return ResponseEntity.ok(notes);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteNote(@PathVariable Long id) {
        noteRepository.deleteById(id); // Delete note by ID
        return ResponseEntity.ok("Note deleted");
    }
}