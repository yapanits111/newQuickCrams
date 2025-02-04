package com.quickcrams.quickcrams;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;

import com.quickcrams.quickcrams.models.User;
import com.quickcrams.quickcrams.repositories.UserRepository;

//@SpringBootApplication
public class UserTest implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    public static void main(String[] args) {
        SpringApplication.run(UserTest.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        // Create a new user
        User user = new User();
        user.setUsername("Daniel");
        user.setPassword("Alex123"); // In a real application, ensure to encode the password

        // Save the user to the database
        userRepository.save(user);

        // Output the saved user
        System.out.println("User  created: " + user.getUsername());
    }
}