import streamlit as st
from utils.constants import ROLES

st.set_page_config(page_title="Login — DelayGuard 360", page_icon="🔐", layout="centered")

st.title("Log in")
st.caption("Select a role to see the workspace built for it. This is a demo — no real credentials are checked.")

tab_login, tab_forgot = st.tabs(["Login", "Forgot password"])

with tab_login:
    email = st.text_input("Work email", placeholder="anita.rao@department.gov")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    role = st.selectbox("Role", ROLES)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login", use_container_width=True, type="primary"):
            st.session_state["role"] = role
            st.session_state["user_email"] = email or "demo@delayguard360.example"
            st.success(f"Logged in as {role}. Use the sidebar to open your dashboard.")
    with c2:
        if st.button("Demo access", use_container_width=True):
            st.session_state["role"] = role
            st.session_state["user_email"] = "demo@delayguard360.example"
            st.success(f"Demo session started as {role}. Use the sidebar to open your dashboard.")

    if st.session_state.get("role"):
        st.info(f"Current session role: **{st.session_state['role']}**")
        page_map = {
            "Admin": "pages/2_Admin_Dashboard.py",
            "Manager": "pages/3_Manager_Dashboard.py",
            "Employee": "pages/4_Employee_Dashboard.py",
            "Citizen": "pages/5_Citizen_Portal.py",
        }
        target = page_map.get(st.session_state["role"])
        if target:
            st.page_link(target, label=f"Go to {st.session_state['role']} dashboard →")

with tab_forgot:
    st.text_input("Enter your work email to receive a reset link", placeholder="anita.rao@department.gov")
    if st.button("Send reset link"):
        st.success("If an account exists for that email, a reset link has been sent.")
