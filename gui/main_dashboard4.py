import streamlit as st
from app.schedule import ScheduleManager
from gui.student_pages4 import show_student_management_page

def launch():
    st.set_page_config(layout="wide", page_title="MSMS Dashboard")

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Student Management", "Daily Roster", "Payments (stub)"]
    )

    if page == "Student Management":
        show_student_management_page(st.session_state.manager)
    elif page == "Daily Roster":
        st.header("Daily Roster")
        st.info("Daily roster page will go here (Fragment 4.3).")
    else:
        st.header("Payments")
        st.info("This feature will be implemented in PST5.")
