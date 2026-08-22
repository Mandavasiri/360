import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_gen import get_data

st.set_page_config(page_title="Admin Dashboard — DelayGuard 360", page_icon="📊", layout="wide")

st.title("Admin dashboard")
st.caption("Full system visibility across every department and request.")

df = get_data()

# ---------- KPI CARDS ----------
total = len(df)
pending = (df["status"] == "In Progress").sum()
completed = (df["status"] == "Completed").sum()
high_risk = (df["risk_level"] == "High").sum()
compliance = round((df["status"] != "Overdue").mean() * 100, 1)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total requests", total)
c2.metric("Pending", pending)
c3.metric("Completed", completed)
c4.metric("High risk", high_risk)
c5.metric("SLA compliance", f"{compliance}%")

st.divider()

# ---------- CHARTS ----------
left, right = st.columns(2)

with left:
    st.markdown("#### SLA compliance trend (by request age, weekly buckets)")
    trend = df.copy()
    trend["week"] = pd.to_datetime(trend["request_date"]).dt.to_period("W").astype(str)
    weekly = trend.groupby("week")["status"].apply(lambda s: round((s != "Overdue").mean() * 100, 1))
    fig = px.line(x=weekly.index, y=weekly.values, markers=True,
                  labels={"x": "Week", "y": "Compliance %"})
    fig.update_traces(line_color="#5B7FFF")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Department performance (avg risk score)")
    dept_avg = df.groupby("department")["risk_score"].mean().sort_values(ascending=False)
    fig2 = px.bar(x=dept_avg.index, y=dept_avg.values,
                  color=dept_avg.values, color_continuous_scale=["#35D0A6", "#F2A93B", "#FF5C5C"],
                  labels={"x": "", "y": "Avg risk score"})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#E8EEF7", coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

left2, right2 = st.columns(2)

with left2:
    st.markdown("#### Risk distribution")
    risk_counts = df["risk_level"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
    fig3 = px.pie(names=risk_counts.index, values=risk_counts.values,
                  color=risk_counts.index,
                  color_discrete_map={"Low": "#35D0A6", "Medium": "#F2A93B", "High": "#FF5C5C"}, hole=0.5)
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7")
    st.plotly_chart(fig3, use_container_width=True)

with right2:
    st.markdown("#### Delay trend by stage")
    stage_avg = df.groupby("current_stage")["risk_score"].mean()
    fig4 = px.bar(x=stage_avg.index, y=stage_avg.values,
                  color=stage_avg.values, color_continuous_scale=["#35D0A6", "#F2A93B", "#FF5C5C"],
                  labels={"x": "", "y": "Avg risk score"})
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#E8EEF7", coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---------- FILTERS + TABLE ----------
st.markdown("#### Recent requests")
f1, f2, f3 = st.columns(3)
dept_filter = f1.multiselect("Department", sorted(df["department"].unique()))
risk_filter = f2.multiselect("Risk level", ["Low", "Medium", "High"])
status_filter = f3.multiselect("Status", sorted(df["status"].unique()))

view = df.copy()
if dept_filter:
    view = view[view["department"].isin(dept_filter)]
if risk_filter:
    view = view[view["risk_level"].isin(risk_filter)]
if status_filter:
    view = view[view["status"].isin(status_filter)]

st.dataframe(
    view[["request_id", "department", "service_type", "current_stage", "assigned_officer",
          "priority", "status", "risk_score", "risk_level"]]
    .sort_values("risk_score", ascending=False)
    .rename(columns={
        "request_id": "Request ID", "department": "Department", "service_type": "Service type",
        "current_stage": "Stage", "assigned_officer": "Officer", "priority": "Priority",
        "status": "Status", "risk_score": "Risk score", "risk_level": "Risk level",
    }),
    use_container_width=True, hide_index=True, height=380,
)
