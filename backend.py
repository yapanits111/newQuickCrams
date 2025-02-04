import sqlite3
import hashlib
import json
import PyPDF2
import spacy
import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet, stopwords

class backendClass:
    def __init__(self, db_path="quickcram.db"):
        self.db_path = db_path
        self.setup_database()
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger_eng')

    def setup_database(self):
        with self.get_db() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS User (
                    userId INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Note (
                    noteId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userId INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS Flashcard (
                    flashcardId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userId INTEGER NOT NULL,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS GeneratedQuiz (
                    genQuizId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userId INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    questions TEXT NOT NULL,
                    pdfName TEXT,
                    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS QuizAttempt (
                    attemptId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userId INTEGER NOT NULL,
                    quizId INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    totalQuestions INTEGER NOT NULL,
                    attemptDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE,
                    FOREIGN KEY (quizId) REFERENCES GeneratedQuiz(genQuizId) ON DELETE CASCADE
                );
            ''')
            conn.commit()  # Ensure changes are saved

    def extract_text_from_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

    def get_wordnet_synonyms(self, word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() != word:
                    synonyms.append(lemma.name())
        return list(set(synonyms))

    def generate_distractors(self, answer, text):
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        
        answer_pos = pos_tag([answer])[0][1]
        similar_words = [word for word, pos in pos_tags if pos == answer_pos and word != answer]
        
        synonyms = self.get_wordnet_synonyms(answer)
        distractors = list(set(similar_words + synonyms))[:3]
        return distractors[:3]

    def generate_questions(self, text, num_questions=5):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        
        questions = []
        important_sentences = []
        
        for sent in doc.sents:
            if sent.ents and len(sent.text.split()) > 5:
                important_sentences.append(sent)
        
        for sent in important_sentences[:num_questions]:
            if not sent.ents:
                continue
                
            answer = max(sent.ents, key=lambda x: len(x.text))
            question_text = sent.text.replace(answer.text, "_____")
            
            options = []
            for ent in doc.ents:
                if ent.label_ == answer.label_ and ent.text != answer.text:
                    options.append(ent.text)
            
            if len(options) < 3:
                options.extend(self.generate_distractors(answer.text, text))
            
            options = list(set(options))[:3]
            options.append(answer.text)
            random.shuffle(options)
            
            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer.text,
                "type": "mcq"
            })
        
        return questions

    def get_db(self):
        return sqlite3.connect(self.db_path)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # User Management
    def create_user(self, username, password):
        try:
            with self.get_db() as conn:
                conn.execute('INSERT INTO User (username, password) VALUES (?, ?)',
                             (username, self.hash_password(password)))
                conn.commit()  # Ensure changes are saved
                return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, str(e)

    def login_user(self, username, password):
        try:
            with self.get_db() as conn:
                hashed_password = self.hash_password(password)
                cursor = conn.execute('SELECT userId, username, password FROM User WHERE username = ?',
                                      (username,))
                user = cursor.fetchone()
                if user and user[2] == hashed_password:
                    return True, {"id": user[0], "username": user[1]}
                return False, "Invalid credentials"
        except Exception as e:
            return False, str(e)

    def get_user(self, user_id):
        try:
            with self.get_db() as conn:
                cursor = conn.execute('SELECT userId, username FROM User WHERE userId = ?', (user_id,))
                user = cursor.fetchone()
                if user:
                    return {"id": user[0], "username": user[1]}
                return None
        except Exception as e:
            return None

    # Notes Management
    def create_note(self, user_id, title, content):
        try:
            with self.get_db() as conn:
                conn.execute('INSERT INTO Note (userId, title, content) VALUES (?, ?, ?)',
                             (user_id, title, content))
                conn.commit()  # Ensure changes are saved
                return True, "Note created successfully"
        except Exception as e:
            return False, str(e)

    def get_notes(self, user_id):
        try:
            with self.get_db() as conn:
                cursor = conn.execute('SELECT * FROM Note WHERE userId = ?', (user_id,))
                notes = cursor.fetchall()
                return [{"noteId": n[0], "userId": n[1], "title": n[2], "content": n[3]} for n in notes]
        except Exception as e:
            return []

    def delete_note(self, note_id, user_id):
        try:
            with self.get_db() as conn:
                conn.execute('DELETE FROM Note WHERE noteId = ? AND userId = ?', (note_id, user_id))
                conn.commit()  # Ensure changes are saved
                return True, "Note deleted successfully"
        except Exception as e:
            return False, str(e)

    # Flashcards Management
    def create_flashcard(self, user_id, front, back):
        try:
            with self.get_db() as conn:
                conn.execute('INSERT INTO Flashcard (userId, front, back) VALUES (?, ?, ?)',
                             (user_id, front, back))
                conn.commit()  # Ensure changes are saved
                return True, "Flashcard created successfully"
        except Exception as e:
            return False, str(e)

    def get_flashcards(self, user_id):
        try:
            with self.get_db() as conn:
                cursor = conn.execute('SELECT * FROM Flashcard WHERE userId = ?', (user_id,))
                cards = cursor.fetchall()
                return [{"cardId": c[0], "userId": c[1], "front": c[2], "back": c[3]} for c in cards]
        except Exception as e:
            return []

    def delete_flashcard(self, card_id, user_id):
        try:
            with self.get_db() as conn:
                conn.execute('DELETE * FROM Flashcard WHERE flashcardId = ? AND userId = ?', (card_id, user_id))
                conn.commit()  # Ensure changes are saved
                return True, "Flashcard deleted successfully"
        except Exception as e:
            return False, str(e)

    def save_generated_quiz(self, user_id, title, questions, pdf_name):
        try:
            formatted_questions = json.dumps([{
                'question': q['question'],
                'options': q['options'],
                'answer': q['answer'],
                'type': 'mcq'
            } for q in questions])

            with self.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO GeneratedQuiz (userId, title, questions, pdfName) VALUES (?, ?, ?, ?)',
                    (user_id, title, formatted_questions, pdf_name)
                )
                conn.commit()
                return True, "Quiz saved successfully"
        except Exception as e:
            print(f"[ERROR] Could not save quiz: {str(e)}")
            return False, str(e)

    def get_generated_quizzes(self, user_id):
        try:
            with self.get_db() as conn:
                cursor = conn.execute('SELECT * FROM GeneratedQuiz WHERE userId = ?', (user_id,))
                quizzes = cursor.fetchall()
                if not quizzes:
                    return []
                    
                formatted_quizzes = []
                for q in quizzes:
                    try:
                        questions = json.loads(q[3])
                        formatted_quizzes.append({
                            "genQuizId": q[0],
                            "userId": q[1],
                            "title": q[2],
                            "questions": questions,
                            "pdfName": q[4]
                        })
                    except json.JSONDecodeError:
                        continue
                return formatted_quizzes
        except Exception as e:
            print(f"Error retrieving quizzes: {str(e)}")
            return []

    def save_quiz_attempt(self, user_id, quiz_id, score, total):
        try:
            with self.get_db() as conn:
                conn.execute(
                    'INSERT INTO QuizAttempt (userId, quizId, score, totalQuestions) VALUES (?, ?, ?, ?)',
                    (user_id, quiz_id, score, total)
                )
                conn.commit()  # Ensure changes are saved
                return True, "Score saved successfully"
        except Exception as e:
            return False, str(e)

    def get_quiz_attempts(self, user_id):
        try:
            with self.get_db() as conn:
                cursor = conn.execute('''
                    SELECT a.*, g.title, g.pdfName 
                    FROM QuizAttempt a 
                    JOIN GeneratedQuiz g ON a.quizId = g.genQuizId 
                    WHERE a.userId = ?
                    ORDER BY a.attemptDate DESC
                ''', (user_id,))
                return cursor.fetchall()
        except Exception as e:
            return []