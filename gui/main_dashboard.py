import streamlit as st
from app.schedule import ScheduleManager
from gui.student_pages import show_student_page
from gui.roster_pages import show_roster_page
from gui.finance_pages import show_finance_page  # <-- add import

def launch():
    st.set_page_config(layout="wide", page_title="Music School Management System")

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio("Go to", ["Student Management", "Daily Roster", "Payments"])

    if page == "Student Management":
        show_student_page(st.session_state.manager)

    elif page == "Daily Roster":
        show_roster_page(st.session_state.manager)
    elif page == "Payments":
        show_finance_page(st.session_state.manager)
