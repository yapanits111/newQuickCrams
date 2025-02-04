package com.quickcrams.quickcrams;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;

import com.quickcrams.quickcrams.models.Note;
import com.quickcrams.quickcrams.repositories.NoteRepository;

//@SpringBootApplication
public class NoteTest implements CommandLineRunner {

    @Autowired
    private NoteRepository noteRepository;

    public static void main(String[] args) {
        SpringApplication.run(NoteTest.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        // Create a new Note
        Note note = new Note();
        note.setTitle("Sample Note Title");
        note.setContent("This is the content of the sample note.");

        // Save the Note to the database
        noteRepository.save(note);

        // Output the saved Note
        System.out.println("Note created: Title = " + note.getTitle() + ", Content = " + note.getContent());
    }
}