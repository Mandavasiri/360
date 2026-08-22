import streamlit as st
import plotly.express as px

from utils.data_gen import get_data
from utils.constants import STAGE_DELAY_HISTORY, DEPARTMENT_DELAY_HISTORY

st.set_page_config(page_title="Bottleneck Analytics — DelayGuard 360", page_icon="🚧", layout="wide")

st.title("Bottleneck analytics")
st.caption("Module 5 — which stage and department are actually causing the delays.")

df = get_data()

top_stage = max(STAGE_DELAY_HISTORY, key=STAGE_DELAY_HISTORY.get)
top_dept = max(DEPARTMENT_DELAY_HISTORY, key=DEPARTMENT_DELAY_HISTORY.get)
avg_hours = df.groupby("current_stage")["hours_used"].mean().get(top_stage, 0)

c1, c2, c3 = st.columns(3)
c1.metric("Top bottleneck stage", top_stage, f"{STAGE_DELAY_HISTORY[top_stage]}% delay rate")
c2.metric("Top delayed department", top_dept, f"{DEPARTMENT_DELAY_HISTORY[top_dept]}% delay rate")
c3.metric("Avg processing time (top stage)", f"{avg_hours:.0f}h")

st.divider()

st.markdown("#### Bottleneck heat map — department × stage (delay %)")

heat = df.copy()
heat["stage_delay"] = heat["current_stage"].map(STAGE_DELAY_HISTORY)
heat["dept_delay"] = heat["department"].map(DEPARTMENT_DELAY_HISTORY)
pivot = heat.pivot_table(
    index="department", columns="current_stage",
    values="risk_score", aggfunc="mean",
).reindex(columns=["Submitted", "Verification", "Approval", "Inspection", "Documentation", "Completion"])

fig = px.imshow(
    pivot, color_continuous_scale=["#101725", "#F2A93B", "#FF5C5C"],
    labels=dict(color="Avg risk score"), aspect="auto",
)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7", height=420)
st.plotly_chart(fig, use_container_width=True)

st.divider()
left, right = st.columns(2)

with left:
    st.markdown("#### Delay trend by stage")
    stage_counts = df["current_stage"].value_counts()
    fig2 = px.bar(x=stage_counts.index, y=stage_counts.values, labels={"x": "", "y": "Requests currently here"})
    fig2.update_traces(marker_color="#F2A93B")
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7")
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.markdown("#### Delay trend by department")
    dept_counts = df[df["status"] == "Overdue"]["department"].value_counts()
    fig3 = px.bar(x=dept_counts.index, y=dept_counts.values, labels={"x": "", "y": "Overdue requests"})
    fig3.update_traces(marker_color="#FF5C5C")
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7")
    st.plotly_chart(fig3, use_container_width=True)
