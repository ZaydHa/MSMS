import streamlit as st
from schedule import ScheduleManager

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
        st.header("Student Management")
        st.info("Student management page will go here (Fragment 4.2).")
    elif page == "Daily Roster":
        st.header("Daily Roster")
        st.info("Daily roster page will go here (Fragment 4.3).")
    else:
        st.header("Payments")
        st.info("This feature will be implemented in PST5.")

