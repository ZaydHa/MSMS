# gui/main_dashboard4.py
import streamlit as st
from app.pst4_manager import ScheduleManager      # <-- adapter
from gui.student_pages4 import show_student_management_page
from gui.roster_pages4 import show_roster_page

def launch():
    st.set_page_config(layout="wide", page_title="MSMS Dashboard")

    # show which class is used (debug helper)
    st.sidebar.caption(f"Manager: {ScheduleManager.__module__}.{ScheduleManager.__name__}")

    # ensure we don't keep an OLD manager from session state
    needs_new = (
        "manager" not in st.session_state or
        getattr(st.session_state["manager"].__class__, "__module__", "") != "app.pst4_manager"
    )
    if needs_new:
        st.session_state.manager = ScheduleManager()


    # optional reset button
    if st.sidebar.button("Reset app"):
        st.session_state.clear()
        st.rerun()

    if st.sidebar.button("Re-seed demo data"):
        st.session_state.manager.reset_demo_data()
        st.success("Demo data has been re-seeded.")
        st.rerun()

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio("Go to", ["Student Management", "Daily Roster", "Payments (stub)"])

    if page == "Student Management":
        show_student_management_page(st.session_state.manager)
    elif page == "Daily Roster":
        show_roster_page(st.session_state.manager)
    else:
        st.header("Payments")
        st.info("This feature will be implemented in PST5.")
