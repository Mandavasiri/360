import streamlit as st
from datetime import datetime

from utils.data_gen import get_data
from utils.constants import DEPARTMENTS, SERVICE_TYPES

st.set_page_config(page_title="Citizen Portal — DelayGuard 360", page_icon="🧾", layout="centered")

st.title("Citizen portal")
st.caption("Submit a request in minutes, and track it without a phone call.")

df = get_data()

tab_submit, tab_track = st.tabs(["Submit a request", "Track a request"])

with tab_submit:
    with st.form("submit_form"):
        name = st.text_input("Full name")
        department = st.selectbox("Department", DEPARTMENTS)
        service = st.selectbox("Service type", SERVICE_TYPES[department])
        details = st.text_area("Describe what you need")
        submitted = st.form_submit_button("Submit request", type="primary")

    if submitted:
        if not name or not details:
            st.error("Enter your name and a short description first.")
        else:
            fake_id = f"REQ-{2000 + hash(name + details) % 900}"
            st.success(f"Request submitted. Your tracking ID is **{fake_id}**.")
            st.info("You'll be notified by email the moment your request's stage changes.")

with tab_track:
    request_id = st.selectbox("Select your request ID", sorted(df["request_id"].unique()))
    row = df[df["request_id"] == request_id].iloc[0]

    st.markdown(f"### {row['request_id']} — {row['service_type']}")
    st.write(f"**Department:** {row['department']}")
    st.write(f"**Status:** {row['status']}")

    stages = ["Submitted", "Verification", "Approval", "Inspection", "Documentation", "Completion"]
    current_idx = stages.index(row["current_stage"])
    st.progress((current_idx + 1) / len(stages), text=f"Current stage: {row['current_stage']}")

    st.caption(f"Expected completion by {row['sla_deadline'].strftime('%d %b %Y')}.")
    if row["status"] == "Overdue":
        st.warning("This request has exceeded its expected processing window. It's been flagged for review.")
