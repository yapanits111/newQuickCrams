import streamlit as st
from front import auth_tabs

def dashboard():
    st.sidebar.title("QuickCram+")
    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Notes", "Flashcards", "Quizzes", "Quiz Generator"]
    )

    if page == "Dashboard":
        st.title("Welcome to QuickCram+ 📚")
        st.write("Use the sidebar to navigate to different sections.")
        st.subheader("Features:")
        st.write("""
        - **Notes**: Create and manage your notes
        - **Flashcards**: Create and manage your flashcards
        - **Quizzes**: Create and take quizzes
        - **Quiz Generator**: Generate quizzes from PDFs
        """)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
            auth_tabs()
                    
    elif page == "Notes":
        from notes import notes
        notes()
    elif page == "Flashcards":
        from flashcards import flashcard
        flashcard()
    elif page == "Quizzes":
        from quiz import quiz
        quiz()
    elif page == "Quiz Generator":
        from quiz_generator import quizGenerator
        quizGenerator()