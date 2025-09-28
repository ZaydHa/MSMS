import streamlit as st
import pandas as pd

def show_roster_page(manager):
    st.header("Daily Roster")

    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    rows = manager.roster_for_day(day)

    if rows:
        # reorder columns for readability if present
        col_order = ["Day", "Time", "Course", "Instrument", "Teacher", "Course ID"]
        df = pd.DataFrame(rows)
        df = df[[c for c in col_order if c in df.columns]]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No lessons for this day.")

    st.subheader("Student Check-in")
    if getattr(manager, "students", None) and getattr(manager, "courses", None):
        student_map = {f"{s.name} (ID {s.id})": s.id for s in manager.students}
        course_map  = {f"{c.name} (ID {c.id})": c.id for c in manager.courses}

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            sel_student = st.selectbox("Student", list(student_map.keys()), key="checkin_student")
        with col2:
            sel_course  = st.selectbox("Course",  list(course_map.keys()),  key="checkin_course")
        with col3:
            status = st.selectbox("Status", ["present", "late", "absent"], key="checkin_status")

        if st.button("Check-in", key="checkin_btn"):
            # If you're using the PST4 adapter, it accepts (student_id, course_id) only.
            # If you later switch to the legacy manager with status support, pass 'status'.
            try:
                ok, msg = manager.check_in(student_map[sel_student], course_map[sel_course])
            except TypeError:
                # legacy manager with status parameter
                ok = manager.check_in(student_map[sel_student], course_map[sel_course], status=status)
                msg = "Check-in recorded." if ok else "Check-in failed."
            (st.success if ok else st.error)(msg)
    else:
        st.info("Add students/courses first.")
