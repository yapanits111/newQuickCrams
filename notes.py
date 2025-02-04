import streamlit as st
from backend import backendClass

back = backendClass()

def notes():
    st.title("📝 Notes")
    
    tab1, tab2 = st.tabs(["My Notes", "Create Note"])
    
    with tab1:
        st.header("My Notes")
        notes = back.get_notes(st.session_state.user['id'])
        
        if notes:
            for note in notes:
                with st.expander(f"Note: {note['title']}"):
                    st.write(note['content'])
                    if note['userId'] == st.session_state.user['id']:
                        if st.button("Delete", key=f"delete_{note['noteId']}"):
                            if st.button("Confirm Delete?", key=f"confirm_{note['noteId']}"):
                                success, message = back.delete_note(
                                    note['noteId'], st.session_state.user['id'])
                                if success:
                                    st.success("Note deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error(message)
        else:
            st.info("No notes yet. Create one in the 'Create Note' tab!")

    with tab2:
        st.header("Create New Note")
        with st.form("note_form"):
            title = st.text_input("Title")
            content = st.text_area("Content")
            
            if st.form_submit_button("Save Note"):
                if title and content:
                    success, message = back.create_note(
                        st.session_state.user['id'], title, content)
                    if success:
                        st.success("Note saved successfully!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")