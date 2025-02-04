import streamlit as st
from backend import backendClass

back = backendClass()

def flashcard():
    st.title("📇 Flashcards")
    
    tab1, tab2 = st.tabs(["My Flashcards", "Create Flashcard"])
    
    with tab1:
        st.header("My Flashcards")
        cards = back.get_flashcards(st.session_state.user['id'])
        
        if cards:
            for card in cards:
                with st.expander(f"Flashcard: {card['front']}"):
                    st.write("**Front:**", card['front'])
                    st.write("**Back:**", card['back'])
                    
                    if card['userId'] == st.session_state.user['id']:
                        if st.button("Delete", key=f"delete_{card['cardId']}"):
                            if st.button("Confirm Delete?", key=f"confirm_{card['cardId']}"):
                                success, message = back.delete_flashcard(
                                    card['cardId'], st.session_state.user['id'])
                                if success:
                                    st.success("Flashcard deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error(message)
        else:
            st.info("No flashcards yet. Create one in the 'Create Flashcard' tab!")

    with tab2:
        st.header("Create New Flashcard")
        with st.form("card_form"):
            front = st.text_input("Front (Question)")
            backPage = st.text_input("Back (Answer)")
            
            if st.form_submit_button("Save Flashcard"):
                if front and backPage:
                    success, message = back.create_flashcard(
                        st.session_state.user['id'], front, backPage)
                    if success:
                        st.success("Flashcard saved successfully!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")