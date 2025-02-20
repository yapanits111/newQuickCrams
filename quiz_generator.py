import streamlit as st
from backend import backendClass

back = backendClass()

def quizGenerator():
    st.title("PDF/Text Quiz Generator")
    
    if "questions" not in st.session_state:
        st.session_state.questions = None
    
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx"])
    
    if uploaded_file:
        text = back.extract_text_from_pdf(uploaded_file)
        
        with st.form(key='generate_quiz_form'):
            num_questions = st.slider("Number of questions", 1, 10, 5)
            generate_button = st.form_submit_button("Generate Quiz")
        
        if generate_button:
            with st.spinner("Generating quiz questions..."):
                questions = back.generate_questions(text, num_questions)
            
            if questions:
                st.session_state.questions = questions
                
                # Show preview
                for i, q in enumerate(questions, 1):
                    st.subheader(f"Question {i}")
                    st.write(q["question"])
                    for opt in q["options"]:
                        st.write(f"- {opt}")
                    with st.expander("Show Answer"):
                        st.write(q["answer"])
    
    if st.session_state.questions:
        with st.form(key='save_quiz_form'):
            title = st.text_input("Quiz Title")
            save_button = st.form_submit_button("Save Quiz")
        
        if save_button:
            if "user" not in st.session_state or "id" not in st.session_state.user:
                st.error("User session not found. Please log in again.")
                return

            if title:
                with st.spinner("Saving quiz to database..."):
                    success, msg = back.save_generated_quiz(
                        st.session_state.user['id'],
                        title,
                        st.session_state.questions,
                        uploaded_file.name
                    )
                if success:
                    st.success("Quiz saved successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Error saving quiz: {msg}")
                    st.error("Please try again")
            else:
                st.error("Please enter a title")

if __name__ == "__main__":
    quizGenerator()