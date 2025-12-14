import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM phishing_logs", conn)
conn.close()

def risk_level(pw_len):
    if pw_len < 8:
        return "🔴 High Risk"
    return "🟡 Medium Risk"

df["Risk Level"] = df["password_length"].apply(risk_level)

print("\n📊 SECURITY AWARENESS REPORT\n")
print(df[["user_id", "email", "Risk Level", "timestamp"]])
