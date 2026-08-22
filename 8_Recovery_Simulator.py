import streamlit as st

from utils.data_gen import get_data
from utils.risk_engine import simulate_recovery, risk_level, risk_color

st.set_page_config(page_title="Recovery Simulator — DelayGuard 360", page_icon="🛠️", layout="centered")

st.title("SLA recovery simulator")
st.caption("Bonus feature — predict the effect of corrective action before you take it.")

df = get_data()
request_id = st.selectbox("Select a request", df.sort_values("risk_score", ascending=False)["request_id"])
row = df[df["request_id"] == request_id].iloc[0]

st.metric("Current risk score", f"{row['risk_score']:.0f}", row["risk_level"])

st.markdown("#### Corrective actions")
extra_officers = st.slider("Additional officers assigned", 0, 5, 0)
priority_boost = st.checkbox("Increase priority to High")

new_score = simulate_recovery(row["risk_score"], extra_officers, priority_boost)
new_level = risk_level(new_score)
improvement = round(row["risk_score"] - new_score, 1)

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Predicted new risk", f"{new_score:.0f}", new_level)
c2.metric("Improvement", f"-{improvement:.0f} pts")
c3.metric("New risk level", new_level)

st.progress(min(new_score / 100, 1.0), text=f"Predicted risk after action: {new_score:.0f}/100 ({new_level})")

if new_level == "Low":
    st.success("These actions bring the request back into a safe SLA range.")
elif new_level == "Medium":
    st.warning("Improved, but still worth monitoring closely.")
else:
    st.error("Still high risk — consider escalation in addition to these actions.")
