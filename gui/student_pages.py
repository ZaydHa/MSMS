import streamlit as st

def show_student_page(manager):
    st.header("Student Management")

    st.subheader("Find a Student")
    query = st.text_input("Search by Name or ID", placeholder="Type a name or student ID")
    if query:
        matches = [
            s for s in manager.students
            if query.lower() in s["name"].lower() or query == str(s["id"])
        ]
        if matches:
            st.table(matches)
        else:
            st.warning("No students found.")

    st.divider()

    # ↓↓↓ YOUR UPDATED REGISTRATION CODE GOES HERE ↓↓↓
    st.subheader("Register a New Student")

    name = st.text_input("New Student Name")
    instrument = st.text_input("First Instrument")

    # Course dropdown
    if manager.courses:
        course_choices = {c["name"]: c["id"] for c in manager.courses}
        course_selected = st.selectbox("Assign to Course", list(course_choices.keys()))
    else:
        st.warning("No courses found. Please add one first.")
        course_selected = None

    if st.button("Register Student"):
        if not name:
            st.error("Please enter a student name.")
        elif not course_selected:
            st.error("Please select a course.")
        else:
            s = manager.add_student(name, f"{name.lower().replace(' ', '.')}@example.com")
            course_id = course_choices[course_selected]
            s["enrolled_course_ids"].append(course_id)
            manager._save_data()
            st.success(f"Registered {s['name']} and enrolled in {course_selected}")
