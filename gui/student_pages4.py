import streamlit as st

def show_student_management_page(manager):
    st.header("Student Management")

    # --- Search by name ---
    with st.expander("Find a student"):
        name_q = st.text_input("Search by name")
        if st.button("Search"):
            s = manager.get_student_by_name(name_q) if name_q else None
            if s:
                st.success(f"Found: {s.name} (ID {s.id}) | Courses: {s.enrolled_course_ids}")
            else:
                st.warning("No match.")

    # --- Register new student ---
    st.subheader("Register New Student")
    with st.form("registration_form", clear_on_submit=True):
        reg_name = st.text_input("Full name")
        reg_instrument = st.text_input("Primary instrument")
        submitted = st.form_submit_button("Register Student")
        if submitted:
            ok, msg, _ = manager.register_new_student(reg_name, reg_instrument)
            (st.success if ok else st.error)(msg)

    # --- Enrol student into course ---
    st.subheader("Enroll student into course")
    if manager.students and manager.courses:
        student_map = {f"{s.name} (ID {s.id})": s.id for s in manager.students}
        course_map  = {f"{c.name} (ID {c.id}) - {c.instrument}": c.id for c in manager.courses}
        sel_student = st.selectbox("Student", list(student_map.keys()))
        sel_course  = st.selectbox("Course",  list(course_map.keys()))
        if st.button("Enroll"):
            ok, msg = manager.enroll_student_in_course(
                student_map[sel_student],
                course_map[sel_course]
            )
            (st.success if ok else st.error)(msg)
    else:
        st.info("Add students/courses first.")
