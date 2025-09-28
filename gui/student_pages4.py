import streamlit as st
import pandas as pd

def show_student_management_page(manager):
    st.header("Student Management")

    # --- Search by name ---
    with st.expander("Find a student", expanded=False):
        name_q = st.text_input("Search by name")
        if st.button("Search", key="search_btn"):
            s = manager.get_student_by_name(name_q.strip()) if name_q else None
            if s:
                st.success(f"Found: {s.name} (ID {s.id})")
                # Show current enrolments if any
                if getattr(s, "enrolled_course_ids", []):
                    rows = []
                    for cid in s.enrolled_course_ids:
                        c = next((c for c in manager.courses if c.id == cid), None)
                        if c:
                            rows.append({"Course": c.name, "Instrument": c.instrument, "Course ID": c.id})
                    if rows:
                        st.dataframe(pd.DataFrame(rows), use_container_width=True)
                else:
                    st.info("No current enrolments.")
            else:
                st.warning("No match.")

    # --- Register new student ---
    st.subheader("Register New Student")
    with st.form("registration_form", clear_on_submit=True):
        reg_name = st.text_input("Full name").strip()
        reg_instrument = st.text_input("Primary instrument").strip()
        submitted = st.form_submit_button("Register Student")
        if submitted:
            if not reg_name or not reg_instrument:
                st.error("Please enter both name and instrument.")
            else:
                ok, msg, _ = manager.register_new_student(reg_name, reg_instrument)
                (st.success if ok else st.error)(msg)

    # --- Enrol student into course ---
    st.subheader("Enroll student into course")
    if getattr(manager, "students", None) and getattr(manager, "courses", None):
        student_map = {f"{s.name} (ID {s.id})": s.id for s in manager.students}
        course_map  = {f"{c.name} (ID {c.id}) - {c.instrument}": c.id for c in manager.courses}
        sel_student = st.selectbox("Student", list(student_map.keys()), key="enrol_student")
        sel_course  = st.selectbox("Course",  list(course_map.keys()),  key="enrol_course")
        can_enrol = bool(sel_student and sel_course)
        if st.button("Enroll", key="enrol_btn", disabled=not can_enrol):
            ok, msg = manager.enroll_student_in_course(
                student_map[sel_student],
                course_map[sel_course]
            )
            (st.success if ok else st.error)(msg)
    else:
        st.info("Add students/courses first.")
