# QuickCram+ Application

QuickCram+ is a web application designed for managing notes, flashcards, and quizzes. It provides a user-friendly interface for users to register, log in, and efficiently organize their study materials.

## Features

- **User Registration and Login**: Secure user authentication with password hashing.
- **Notes Management**: Create, view, and delete personal notes.
- **Flashcards**: Create and manage flashcards for quick revision.
- **Quizzes**: Create quizzes with multiple-choice questions and track results.

## Technologies Used

- Python
- Streamlit
- SQLite
- hashlib (for password hashing)

## Setup Instructions

1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd quickcram-app
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Start the Streamlit application with:
   ```
   streamlit run frontend.py
   ```

4. **Access the Application**:
   Open your web browser and go to `http://localhost:8501` to access the QuickCram+ application.

## Usage Guidelines

- **Registration**: Create a new account by providing a unique username and password.
- **Login**: Use your credentials to log in and access your dashboard.
- **Dashboard Navigation**: Use the sidebar to navigate between Notes, Flashcards, and Quizzes.
- **Creating Entries**: Use the respective tabs to create new notes, flashcards, or quizzes.
- **Deleting Entries**: You can delete any note, flashcard, or quiz by confirming the deletion.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.