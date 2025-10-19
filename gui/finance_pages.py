import streamlit as st

def show_finance_page(manager):
    st.header("Finance & Payments")

    if not manager.students:
        st.info("Add a student first.")
        return

    # --- Record New Payment ---
    st.subheader("Record New Payment")
    student_map = {s["name"]: s["id"] for s in manager.students}
    with st.form("payment_form"):
        sname = st.selectbox("Student", list(student_map.keys()))
        amount = st.number_input("Amount (AUD)", min_value=0.0, step=1.0, format="%.2f")
        method = st.text_input("Method (e.g., Cash, Card, Bank)")
        submitted = st.form_submit_button("Record Payment")
        if submitted:
            ok = manager.record_payment(student_map[sname], amount, method)
            st.success(f"Recorded ${amount:.2f} via {method} for {sname}") if ok else st.error("Payment failed.")

    st.divider()

    # --- Payment History ---
    st.subheader("View Payment History")
    sname2 = st.selectbox("Select Student", list(student_map.keys()), key="history_select")
    sid = student_map[sname2]
    history = manager.get_payment_history(sid)
    if history:
        st.caption(f"{len(history)} payment(s) found.")
        st.table(history)
    else:
        st.info("No payments for this student.")

    st.divider()

    # --- Export Reports ---
    st.subheader("Export Reports (CSV)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Payments CSV"):
            st.success("Exported to payments_report.csv") if manager.export_report("payments", "payments_report.csv") else st.error("Export failed.")
    with col2:
        if st.button("Export Attendance CSV"):
            st.success("Exported to attendance_report.csv") if manager.export_report("attendance", "attendance_report.csv") else st.error("Export failed.")
