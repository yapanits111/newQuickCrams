package com.quickcrams.quickcrams;

import java.util.Arrays;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;

import com.quickcrams.quickcrams.models.Quiz;
import com.quickcrams.quickcrams.repositories.QuizRepository;

//@SpringBootApplication
public class QuizTest implements CommandLineRunner {

    @Autowired
    private QuizRepository quizRepository;

    public static void main(String[] args) {
        SpringApplication.run(QuizTest.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
    // Create a new Quiz
    Quiz quiz = new Quiz();
    quiz.setQuestions("Sample Question");
    quiz.setChoices(Arrays.asList("Choice 1", "Choice 2", "Choice 3"));
    quiz.setAnswer("Choice 1");

    // Save the Quiz to the database
    quizRepository.save(quiz);

    // Fetch and output the saved Quiz
    Quiz savedQuiz = quizRepository.findById(quiz.getId()).orElse(null);
    System.out.println("Quiz created: Questions = " + savedQuiz.getQuestions() +
        ", Choices = " + savedQuiz.getChoices() + ", Answer = " + savedQuiz.getAnswer());
}

}
