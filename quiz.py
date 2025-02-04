import streamlit as st
import pandas as pd
from backend import backendClass

back = backendClass()

def take_quiz(quiz):
    st.subheader(f"Taking Quiz: {quiz['title']}")
    questions = quiz['questions']

    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    for i, q in enumerate(questions):
        st.write(f"Question {i + 1}/{len(questions)}")
        st.write(q["question"])
        st.session_state.answers[i] = st.radio(f"Choose your answer for question {i + 1}:", q["options"], key=f"answer_{quiz['genQuizId']}_{i}")

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
        
        if quizzes:
            for quiz in quizzes:
                if st.button(f"Take Quiz: {quiz['title']}", key=f"take_{quiz['genQuizId']}"):
                    st.session_state.current_quiz = quiz
                    st.rerun()
        
        if 'current_quiz' in st.session_state:
            take_quiz(st.session_state.current_quiz)
    
    with tab2:
        results = back.get_quiz_attempts(st.session_state.user['id'])
        if results:
            df = pd.DataFrame(results, columns=['ID', 'User', 'Quiz', 'Score', 'Total', 'Date', 'Title', 'PDF'])
            st.dataframe(df[['Title', 'Score', 'Total', 'Date']], hide_index=True)

if __name__ == "__main__":
    quiz()