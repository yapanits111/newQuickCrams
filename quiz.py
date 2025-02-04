import streamlit as st
import pandas as pd
from backend import backendClass

back = backendClass()

def take_quiz(quiz):
    st.subheader(f"Taking Quiz: {quiz['title']}")
    questions = quiz['questions']
    
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
        st.session_state.score = 0
        
    if st.session_state.current_q < len(questions):
        q = questions[st.session_state.current_q]
        st.write(f"Question {st.session_state.current_q + 1}/{len(questions)}")
        st.write(q["question"])
        
        # Handle MCQ format
        answer = st.radio("Choose your answer:", q["options"])
        
        if st.button("Submit Answer"):
            if answer == q["answer"]:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The answer was: {q['answer']}")
            
            st.session_state.current_q += 1
            
            # Save quiz attempt when completed
            if st.session_state.current_q >= len(questions):
                back.save_quiz_attempt(
                    st.session_state.user['id'],
                    quiz['genQuizId'],
                    st.session_state.score,
                    len(questions)
                )
                st.success(f"Quiz completed! Score: {st.session_state.score}/{len(questions)}")
                if st.button("Return to Quizzes"):
                    del st.session_state.current_q
                    del st.session_state.score
                    st.rerun()
            else:
                st.rerun()

def quiz():
    st.title("📝 Quiz Application")
    
    tab1, tab2 = st.tabs(["Available Quizzes", "Quiz Results"])
    
    with tab1:
        quizzes = back.get_generated_quizzes(st.session_state.user['id'])
        
        if quizzes:
            for quiz in quizzes:
                col1, col2 = st.columns([3,1])
                with col1:
                    st.subheader(quiz['title'])
                with col2:
                    if st.button("Take Quiz", key=f"take_{quiz['genQuizId']}"):
                        take_quiz(quiz)
    
    with tab2:
        results = back.get_quiz_attempts(st.session_state.user['id'])
        if results:
            df = pd.DataFrame(results, columns=['ID', 'User', 'Quiz', 'Score', 'Total', 'Date', 'Title', 'PDF'])
            st.dataframe(df[['Title', 'Score', 'Total', 'Date']])