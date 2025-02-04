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
        
        # Add debug print
        st.write(f"Debug - Saving quiz attempt: user={st.session_state.user['id']}, quiz={quiz['genQuizId']}, score={score}, total={len(questions)}")
        
        success, message = back.save_quiz_attempt(
            st.session_state.user['id'],
            quiz['genQuizId'],
            score,
            len(questions)
        )
        
        if success:
            st.success(f"Quiz completed! Score: {score}/{len(questions)}")
        else:
            st.error(f"Failed to save quiz result: {message}")

        if st.button("Return to Quizzes"):
            del st.session_state.answers
            del st.session_state.score
            st.rerun()

def quiz():
    st.title("📝 Quiz Application")
    
    tab1, tab2 = st.tabs(["Available Quizzes", "Quiz Results"])
    
    with tab1:
        quizzes = back.get_generated_quizzes(st.session_state.user['id'])
        
        # Convert list to DataFrame if needed
        if isinstance(quizzes, list):
            quizzes = pd.DataFrame(quizzes)
        
        if not quizzes.empty:
            st.subheader("Available Quizzes")
            quizzes_display = pd.DataFrame({
                'Title': quizzes['title'],
                'PDF Name': quizzes['pdfName']
            })
            
            selected_quiz = st.selectbox("Select a Quiz", quizzes_display['Title'].tolist())

            if st.button("Take Selected Quiz"):
                selected_quiz_row = quizzes[quizzes['title'] == selected_quiz]
                if not selected_quiz_row.empty:
                    st.session_state.current_quiz = selected_quiz_row.iloc[0]
                    st.rerun()
        
        if 'current_quiz' in st.session_state:
            take_quiz(st.session_state.current_quiz)
    
    with tab2:
        results = back.get_quiz_attempts(st.session_state.user['id'])
    
        if not results.empty:
            st.subheader("Quiz Results")

            #Legend
            st.write("Legend:")
            st.write("- Perfect: 100%")
            st.write("- Passed: 75 to 99%")
            st.write("- Study Harder: Below 75%")
        
            # Create a DataFrame from the results data
            df = results.copy()
            df.columns = ['Attempt ID', 'Score', 'Total', 'Date', 'Quiz']
        
            # Calculate percentage and grade
            df['Percentage'] = (df['Score'] / df['Total']) * 100
            df['Grade'] = df.apply(
                lambda row: 'Perfect' if row['Score'] == row['Total']
                else 'Passed' if row['Percentage'] >= 75
                else 'Study Harder',
                axis=1
            )
        
            # Display DataFrame
            st.dataframe(
                df[['Quiz', 'Score', 'Total', 'Date', 'Grade']], 
                height=600, 
                width=1000,
                hide_index=True
            )
        else:
            st.info("No quiz attempts found")

if __name__ == "__main__":
    quiz()