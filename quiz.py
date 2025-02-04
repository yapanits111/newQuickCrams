import streamlit as st
import pandas as pd
from backend import backendClass
import json

back = backendClass()

def take_quiz(quiz):
    st.subheader(f"Taking Quiz: {quiz['title']}")
    
    # Handle questions data based on type
    questions = quiz['questions']
    if isinstance(questions, str):
        questions = json.loads(questions)
    elif isinstance(questions, list):
        questions = questions

    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    for i, q in enumerate(questions):
        st.write(f"Question {i + 1}/{len(questions)}")
        st.write(q["question"])
        st.session_state.answers[i] = st.radio(
            f"Choose your answer for question {i + 1}:", 
            q["options"], 
            key=f"answer_{quiz['genQuizId']}_{i}"
        )

    submit_button = st.button("Submit Answers", key=f"submit_{quiz['genQuizId']}")

    if submit_button:
        score = 0
        for i, q in enumerate(questions):
            if st.session_state.answers[i] == q["answer"]:
                score += 1

        st.session_state.score = score
        st.success(f"Quiz completed! Score: {score}/{len(questions)}")

        back.save_quiz_attempt(
            st.session_state.user['id'],
            quiz['genQuizId'],
            score,
            len(questions)
        )

        if st.button("Return to Quizzes"):
            del st.session_state.answers
            del st.session_state.score
            st.rerun()

def quiz():
    st.title("📝 Quiz Application")
    
    tab1, tab2 = st.tabs(["Available Quizzes", "Quiz Results"])
    
    with tab1:
        quizzes = back.get_generated_quizzes(st.session_state.user['id'])
        
        if len(quizzes) > 0:  # Check if DataFrame has rows
            st.subheader("Available Quizzes")
            quizzes_display = quizzes[['title', 'pdfName']]
            quizzes_display.columns = ['Title', 'PDF Name']
            quizzes_display.reset_index(drop=True, inplace=True)
            
            if len(quizzes_display) > 0:
                selected_quiz = st.selectbox("Select a Quiz", quizzes_display['Title'].tolist())

                if st.button("Take Selected Quiz"):
                    selected_quiz_row = quizzes[quizzes['title'] == selected_quiz]
                    if len(selected_quiz_row) > 0:
                        st.session_state.current_quiz = selected_quiz_row.iloc[0]
                        st.rerun()
        
        if 'current_quiz' in st.session_state:
            take_quiz(st.session_state.current_quiz)
    
    with tab2:
        results = back.get_quiz_attempts(st.session_state.user['id'])
        if len(results) > 0:
            st.subheader("Quiz Results")

            st.write("Legend:")
            st.write("Excellent: 100%", color="green")
            st.write("Passed: 75 - 99%", color="yellow")
            st.write("Study Harder: below 75%", color="red")

            # Create a DataFrame from the results data
            df = results.copy()  # Create a copy to avoid modifying original
            df.columns = ['Attempt ID', 'Score', 'Total', 'Date', 'Quiz']  # Rename columns
            df['Conclusion'] = df.apply(
                lambda row: 'Excellent' if row['Score'] == row['Total'] 
                else 'Passed' if row['Score'] >= 0.75 * row['Total'] 
                else 'Study Harder', 
                axis=1
            )
            
            # Display the DataFrame
            st.dataframe(
                df[['Quiz', 'Score', 'Total', 'Date', 'Conclusion']], 
                height=600, 
                width=1000,
                hide_index=True 
            )

if __name__ == "__main__":
    quiz()