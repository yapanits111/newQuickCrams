import streamlit as st
import dashboard
from backend import backendClass

back = backendClass()

def mainPage():
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    st.set_page_config(page_title="QuickCram+", page_icon="📚", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        dashboard.dashboard()
    else:
        auth_tabs()

def auth_tabs():
    st.title("QuickCram+ 📚")
    tabs = st.tabs(["Login", "Sign Up"])

    with tabs[0]:
        login()

    with tabs[1]:
        signup()

def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")  # Ensure password is captured
    
    if st.button("Login"):
        if username and password:  # Check both fields are filled
            success, response = back.login_user(username, password)  # Pass both arguments
            if success:
                st.session_state.logged_in = True
                st.session_state.user = response
                st.rerun()
            else:
                st.error(response)
        else:
            st.error("Please fill in all fields")

def signup():
    st.title("Sign Up")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            print(f"Signup attempt: {username}")
            if not all([username, password]):
                st.error("Please fill in all fields")
            else:
                success, message = back.create_user(username, password)
                if success:
                    st.success("Registration successful! Please login.")
                else:
                    st.error(message or "Username already exists")

if __name__ == "__main__":
    mainPage()