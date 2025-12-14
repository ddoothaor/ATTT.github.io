import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
# CONFIG
DB_PATH = "database.db"
ADMIN_PASSWORD = "admin123"
# DATABASE INIT

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS phishing_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            email TEXT,
            password_length INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
# STREAMLIT UI
st.set_page_config(
    page_title="Security Awareness Training System",
    page_icon="🔐"
)

st.title("🔐 Security Awareness Training System")
st.caption("Phishing Simulation & Awareness Monitoring (Educational Purpose)")

# ROLE SELECTION
role = st.radio(
    "Select your role",
    ["👨‍💼 Employee", "🛡️ Admin"]
)
# EMPLOYEE FLOW
if role == "👨‍💼 Employee":
    st.subheader("🎣 Corporate Login Page (Simulation)")

    user_id = st.text_input("Employee ID", value="EMP1023")
    email = st.text_input("Corporate Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO phishing_logs (user_id, email, password_length, timestamp)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                email,
                len(password),
                datetime.now().isoformat()
            ))
            conn.commit()
            conn.close()

            st.error(
                "⚠️ This was a phishing simulation.\n\n"
                "Your credential submission has been recorded for "
                "security awareness training purposes."
            )
        else:
            st.warning("Please fill in all required fields.")

# ADMIN FLOW
if role == "🛡️ Admin":
    st.subheader("🛡️ Admin Authentication")

    admin_pw = st.text_input("Admin Password", type="password")

    if admin_pw == ADMIN_PASSWORD:
        st.success("Admin authenticated successfully")

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM phishing_logs", conn)
        conn.close()

        if df.empty:
            st.info("No phishing incidents recorded yet.")
        else:
            def risk_level(pw_len):
                if pw_len < 8:
                    return "🔴 High Risk (Weak Password)"
                return "🟡 Medium Risk"

            df["Risk Level"] = df["password_length"].apply(risk_level)

            st.markdown("### 📊 Phishing Incident Report")
            st.dataframe(
                df[["user_id", "email", "Risk Level", "timestamp"]],
                use_container_width=True
            )

            st.markdown("### 📈 Risk Distribution")
            st.bar_chart(df["Risk Level"].value_counts())

            st.markdown("""
            **Interpretation:**
            - 🔴 High Risk: Employee submitted credentials using a weak password  
            - 🟡 Medium Risk: Credentials submitted but password length acceptable  
            """)
    elif admin_pw:
        st.error("❌ Incorrect admin password")
