import streamlit as st

def show_roster_page(manager):
    st.header("Daily Roster / Check-in")

    if not manager.students or not manager.courses:
        st.info("You need at least one student and one course.")
        return

    # --- FIXED: use 'name' instead of 'title'
    student_map = {f'{s.get("name", "Unnamed")} (id {s.get("id", "?")})': s.get("id") for s in manager.students}
    course_map = {
    f"{c.get('name', 'Untitled Course')} (id {c.get('id', '?')})": c.get('id')
    for c in manager.courses
}

    col1, col2, col3 = st.columns([4, 4, 1])
    with col1:
        ssel = st.selectbox("Student", list(student_map.keys()), key="roster_s")
    with col2:
        csel = st.selectbox("Course", list(course_map.keys()), key="roster_c")
    with col3:
        if st.button("Check-in"):
            sid = student_map[ssel]
            cid = course_map[csel]
            student = next((x for x in manager.students if x["id"] == sid), None)
            if not student:
                st.error("Student not found.")
                return
            if cid not in student.get("enrolled_course_ids", []):
                st.warning("This student is not enrolled in that course.")
                return
            ok = manager.check_in(sid, cid)
            st.success("Checked in!") if ok else st.error("Check-in failed.")

    st.divider()
    st.subheader("Recent Attendance")
    if manager.attendance:
        rows = manager.attendance[-20:][::-1]
        st.table(rows)
    else:
        st.caption("No attendance yet.")
