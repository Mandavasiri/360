import streamlit as st
import plotly.express as px

from utils.data_gen import get_data

st.set_page_config(page_title="Manager Dashboard — DelayGuard 360", page_icon="👥", layout="wide")

st.title("Manager dashboard")
st.caption("Team-level control: workload, escalation, and department SLA health.")

df = get_data()

c1, c2, c3 = st.columns(3)
c1.metric("Team requests", len(df))
c2.metric("Critical requests", (df["risk_level"] == "High").sum())
c3.metric("Overdue", (df["status"] == "Overdue").sum())

st.divider()

left, right = st.columns([1, 1])

with left:
    st.markdown("#### Workload by officer")
    workload = df["assigned_officer"].value_counts().sort_values(ascending=True).tail(10)
    fig = px.bar(x=workload.values, y=workload.index, orientation="h",
                 labels={"x": "Open requests", "y": ""})
    fig.update_traces(marker_color="#5B7FFF")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Department SLA health")
    dept_health = df.groupby("department").apply(lambda d: round((d["status"] != "Overdue").mean() * 100, 1))
    fig2 = px.bar(x=dept_health.index, y=dept_health.values,
                  color=dept_health.values, color_continuous_scale=["#FF5C5C", "#F2A93B", "#35D0A6"],
                  labels={"x": "", "y": "SLA compliance %"})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#E8EEF7", coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.markdown("#### Critical requests — take action")

critical = df[df["risk_level"] == "High"].sort_values("risk_score", ascending=False).head(15)

for _, row in critical.iterrows():
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 2])
        c1.write(f"**{row['request_id']}** · {row['department']}")
        c2.write(f"{row['current_stage']} · {row['assigned_officer']}")
        c3.write(f":red[{row['risk_score']:.0f}]")
        with c4:
            b1, b2, b3 = st.columns(3)
            if b1.button("Escalate", key=f"esc_{row['request_id']}"):
                st.toast(f"{row['request_id']} escalated to supervisor.")
            if b2.button("Reassign", key=f"reas_{row['request_id']}"):
                st.toast(f"{row['request_id']} queued for reassignment.")
            if b3.button("Approve", key=f"appr_{row['request_id']}"):
                st.toast(f"{row['request_id']} approved to next stage.")
