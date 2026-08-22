import streamlit as st
import pandas as pd

from utils.data_gen import get_data
from utils.constants import STAGES

st.set_page_config(page_title="Employee Dashboard — DelayGuard 360", page_icon="🧑‍💼", layout="wide")

st.title("Employee dashboard")
st.caption("A focused queue — only what's assigned to you, nothing from other teams.")

df = get_data()
officer = st.selectbox("Viewing queue for", sorted(df["assigned_officer"].unique()))
mine = df[df["assigned_officer"] == officer].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Assigned", len(mine))
c2.metric("Pending", (mine["status"] == "In Progress").sum())
c3.metric("Due today", (mine["hours_used"] >= mine["sla_hours"] * 0.9).sum())
c4.metric("Completed", (mine["status"] == "Completed").sum())

st.divider()
st.markdown("#### My requests")

for _, row in mine.sort_values("risk_score", ascending=False).iterrows():
    with st.container(border=True):
        top = st.columns([2, 2, 2, 2, 2])
        top[0].write(f"**{row['request_id']}**")
        top[1].write(row["service_type"])
        top[2].write(f"Stage: {row['current_stage']}")
        top[3].write(f"Priority: {row['priority']}")
        badge = {"Low": "🟢", "Medium": "🟠", "High": "🔴"}[row["risk_level"]]
        top[4].write(f"{badge} {row['risk_score']:.0f} risk")

        bottom = st.columns([3, 2])
        current_idx = STAGES.index(row["current_stage"])
        new_stage = bottom[0].selectbox(
            "Update stage", STAGES, index=current_idx, key=f"stage_{row['request_id']}", label_visibility="collapsed"
        )
        if bottom[1].button("Save update", key=f"save_{row['request_id']}"):
            st.toast(f"{row['request_id']} moved to {new_stage}.")
        if row["current_stage"] != "Completion":
            if bottom[1].button("Mark complete", key=f"done_{row['request_id']}"):
                st.toast(f"{row['request_id']} marked complete.")
