package com.quickcrams.quickcrams.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.quickcrams.quickcrams.models.Quiz;
import com.quickcrams.quickcrams.models.QuizResult;
import com.quickcrams.quickcrams.repositories.QuizRepository;
import com.quickcrams.quickcrams.repositories.QuizResultRepository;

@RestController
@RequestMapping("/api/quiz")
public class QuizController {

    @Autowired
    private QuizRepository quizRepository;

    @Autowired
    private QuizResultRepository quizResultRepository;

    @PostMapping
    public ResponseEntity<String> createQuiz(@RequestBody Quiz quiz) {
        quizRepository.save(quiz); // Save quiz to the database
        return ResponseEntity.ok("Quiz created");
    }

    @PostMapping("/results")
    public ResponseEntity<String> submitQuizResults(@RequestBody QuizResult quizResult) {
        quizResultRepository.save(quizResult); // Save quiz results to the database
        return ResponseEntity.ok("Quiz results submitted");
    }

    @GetMapping("/results")
    public ResponseEntity<List<QuizResult>> getQuizResults() {
        List<QuizResult> results = quizResultRepository.findAll(); // Retrieve quiz results
        return ResponseEntity.ok(results);
    }
}