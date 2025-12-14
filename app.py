import streamlit as st
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database.db")
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

st.set_page_config(page_title="Company Secure Login", page_icon="🔐")

st.title("🔐 Company Internal System")
st.caption("Security Awareness Training Simulation")

user_id = "EMP1023" 
email = st.text_input("Corporate Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if email and password:
        conn = sqlite3.connect("database.db")
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

        st.error("⚠️ This was a phishing. You have submitted credentials.")
    else:
        st.warning("Please enter email and password.")
