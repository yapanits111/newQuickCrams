package com.quickcrams.quickcrams;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;

import com.quickcrams.quickcrams.models.QuizResult;
import com.quickcrams.quickcrams.repositories.QuizResultRepository;

//@SpringBootApplication
public class QuizResultTest implements CommandLineRunner {

    @Autowired
    private QuizResultRepository quizResultRepository;

    public static void main(String[] args) {
        SpringApplication.run(QuizResultTest.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        // Create a new QuizResult
        QuizResult quizResult = new QuizResult();
        quizResult.setUserId(1L); // Assuming a user with ID 1 exists
        quizResult.setQuizId(1L); // Assuming a quiz with ID 1 exists
        quizResult.setScore(85);   // Example score

        // Save the QuizResult to the database
        quizResultRepository.save(quizResult);

        // Output the saved QuizResult
        System.out.println("QuizResult created: User ID = " + quizResult.getUserId() + ", Quiz ID = " + quizResult.getQuizId() + ", Score = " + quizResult.getScore());
    }
}