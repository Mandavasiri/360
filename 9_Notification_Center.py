import streamlit as st

from utils.data_gen import get_data

st.set_page_config(page_title="Notification Center — DelayGuard 360", page_icon="🔔", layout="wide")

st.title("Notification center")
st.caption("Module 7 — Early Warning System. High-risk, critical, and escalation alerts.")

df = get_data()

high = df[df["risk_level"] == "High"].sort_values("risk_score", ascending=False)
critical = df[df["risk_score"] >= 90]
overdue = df[df["status"] == "Overdue"]

c1, c2, c3 = st.columns(3)
c1.metric("High risk alerts", len(high))
c2.metric("Critical alerts", len(critical))
c3.metric("Escalation alerts (overdue)", len(overdue))

st.divider()

tab1, tab2, tab3 = st.tabs(["High risk", "Critical", "Escalation"])

with tab1:
    for _, r in high.iterrows():
        st.warning(f"**{r['request_id']}** ({r['department']}) — risk {r['risk_score']:.0f}/100, currently at {r['current_stage']}.")

with tab2:
    if critical.empty:
        st.write("No critical alerts right now.")
    for _, r in critical.iterrows():
        st.error(f"**{r['request_id']}** ({r['department']}) — risk {r['risk_score']:.0f}/100. Immediate escalation recommended.")

with tab3:
    for _, r in overdue.iterrows():
        st.error(f"**{r['request_id']}** ({r['department']}) — SLA deadline passed on {r['sla_deadline'].strftime('%d %b %Y')}. Escalate to supervisor.")
