package com.quickcrams.quickcrams.models;

import java.util.List;
import jakarta.persistence.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

@Entity
public class Quiz {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String questions;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String choices;
    private String answer;

    public void setChoices(List<String> choices) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            this.choices = objectMapper.writeValueAsString(choices);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Error converting list to JSON", e);
        }
    }

    public List<String> getChoices() {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            return objectMapper.readValue(this.choices, new TypeReference<List<String>>() {});
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Error converting JSON to list", e);
        }
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getQuestions() { return questions; }
    public void setQuestions(String questions) { this.questions = questions; }
    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }
}