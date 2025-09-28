import streamlit as st
import pandas as pd

def show_roster_page(manager):
    st.header("Daily Roster")

    day = st.selectbox(
        "Select a day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )
    rows = manager.roster_for_day(day)
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No lessons for this day.")

    st.subheader("Student Check-in")
    if manager.students and manager.courses:
        student_map = {f"{s.name} (ID {s.id})": s.id for s in manager.students}
        course_map  = {f"{c.name} (ID {c.id})": c.id for c in manager.courses}
        sel_student = st.selectbox("Student", list(student_map.keys()), key="checkin_student")
        sel_course  = st.selectbox("Course",  list(course_map.keys()),  key="checkin_course")
        if st.button("Check-in"):
            ok, msg = manager.check_in(student_map[sel_student], course_map[sel_course])
            (st.success if ok else st.error)(msg)
    else:
        st.info("Add students/courses first.")
