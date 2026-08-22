import streamlit as st
import plotly.express as px

from utils.data_gen import get_data

st.set_page_config(
    page_title="DelayGuard 360",
    page_icon="🛡️",
    layout="wide",
)

# ---------- THEME / STYLE ----------
st.markdown("""
<style>
.stApp { background-color: #0A0E14; }
h1, h2, h3 { font-family: 'Trebuchet MS', sans-serif; }
.metric-box {
    background:#101725; border:1px solid #223046; border-radius:10px;
    padding:16px 18px; text-align:center;
}
.metric-num { font-size:30px; font-weight:700; color:#E8EEF7; }
.metric-label { font-size:12px; color:#8B98AC; text-transform:uppercase; letter-spacing:0.05em; }
.eyebrow {
    display:inline-block; color:#F2A93B; border:1px solid rgba(242,169,59,0.35);
    background:rgba(242,169,59,0.08); padding:4px 12px; border-radius:16px;
    font-size:12px; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

df = get_data()

st.markdown('<div class="eyebrow">Predictive SLA intelligence</div>', unsafe_allow_html=True)
st.title("DelayGuard 360")
st.subheader("From delay detection to delay prevention.")
st.write(
    "DelayGuard 360 watches every service request in flight, predicts which ones will "
    "breach SLA, explains exactly why, and recommends the fix — while there's still time to act."
)

st.divider()

# ---------- KPI ROW ----------
total = len(df)
pending = (df["status"] == "In Progress").sum()
completed = (df["status"] == "Completed").sum()
high_risk = (df["risk_level"] == "High").sum()
compliance = round((df["status"] != "Overdue").mean() * 100, 1)

cols = st.columns(5)
kpis = [
    ("Total requests", total),
    ("Pending", pending),
    ("Completed", completed),
    ("High risk", high_risk),
    ("SLA compliance", f"{compliance}%"),
]
for c, (label, value) in zip(cols, kpis):
    c.markdown(
        f'<div class="metric-box"><div class="metric-num">{value}</div>'
        f'<div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# ---------- CHARTS PREVIEW ----------
c1, c2 = st.columns(2)

with c1:
    st.markdown("##### Risk distribution")
    risk_counts = df["risk_level"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
    fig = px.pie(
        names=risk_counts.index, values=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map={"Low": "#35D0A6", "Medium": "#F2A93B", "High": "#FF5C5C"},
        hole=0.55,
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EEF7", showlegend=True, height=320)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("##### Department delay rate")
    dept_avg = df.groupby("department")["risk_score"].mean().sort_values(ascending=True)
    fig2 = px.bar(
        x=dept_avg.values, y=dept_avg.index, orientation="h",
        color=dept_avg.values, color_continuous_scale=["#35D0A6", "#F2A93B", "#FF5C5C"],
        labels={"x": "Avg risk score", "y": ""},
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#E8EEF7", coloraxis_showscale=False, height=320)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.markdown("##### Get started")
st.write(
    "Use the sidebar to log in with a role, then head to your dashboard. "
    "Try **Demo Access** on the Login page to jump straight in without entering credentials."
)
st.page_link("pages/1_Login.py", label="Go to Login →", icon="🔐")
