import streamlit as st
import plotly.graph_objects as go

from utils.data_gen import get_data
from utils.explain import explain_risk, case_summary
from utils.recommend import recommend_actions
from utils.risk_engine import risk_color
from utils.constants import STAGE_DELAY_HISTORY, DEPARTMENT_DELAY_HISTORY, PRIORITY_IMPACT

st.set_page_config(page_title="Risk Analysis — DelayGuard 360", page_icon="🧠", layout="wide")

st.title("Risk analysis")
st.caption("Explainable AI (Module 3) + Recommendation engine (Module 4), per request.")

df = get_data()
request_id = st.selectbox("Select a request", df.sort_values("risk_score", ascending=False)["request_id"])
row = df[df["request_id"] == request_id].iloc[0]

c1, c2 = st.columns([1, 2])

with c1:
    color = risk_color(row["risk_level"])
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=row["risk_score"],
        number={"suffix": " / 100", "font": {"color": "#E8EEF7"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#8B98AC"},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40], "color": "rgba(53,208,166,0.15)"},
                {"range": [40, 70], "color": "rgba(242,169,59,0.15)"},
                {"range": [70, 100], "color": "rgba(255,92,92,0.15)"},
            ],
        },
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7", height=280,
                       margin=dict(t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**Risk level:** :orange[{row['risk_level']}]" if row["risk_level"] == "Medium"
                else (f"**Risk level:** :red[{row['risk_level']}]" if row["risk_level"] == "High"
                      else f"**Risk level:** :green[{row['risk_level']}]"))

with c2:
    st.markdown("#### Score breakdown")
    breakdown = {
        "SLA usage (40%)": row["sla_usage_pct"] * 0.4,
        "Stage delay history (30%)": STAGE_DELAY_HISTORY[row["current_stage"]] * 0.3,
        "Department delay history (20%)": DEPARTMENT_DELAY_HISTORY[row["department"]] * 0.2,
        "Priority impact (10%)": PRIORITY_IMPACT[row["priority"]] * 0.1,
    }
    fig2 = go.Figure(go.Bar(
        x=list(breakdown.values()), y=list(breakdown.keys()), orientation="h",
        marker_color=["#5B7FFF", "#F2A93B", "#35D0A6", "#8B98AC"],
    ))
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#E8EEF7", height=280, margin=dict(t=10, b=10),
                        xaxis_title="Contribution to risk score")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Why this is risky")
    for reason in explain_risk(row):
        st.write(f"- {reason}")

with col2:
    st.markdown("#### Recommended actions")
    for action in recommend_actions(row):
        st.write(f"- {action}")

st.divider()
st.markdown("#### AI case summary")
st.info(case_summary(row))
