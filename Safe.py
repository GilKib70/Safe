import streamlit as st
import pandas as pd
import plotly.express as px

# ===== MOCK DATA =====
def get_data():
    return {
        "threats": pd.DataFrame({
            "Time": ["10:00", "11:30", "13:45"],
            "Type": ["Phishing", "Malware", "Brute Force"],
            "Severity": ["High", "Critical", "Medium"]
        }),
        "kpis": {
            "active_threats": 3,
            "secured_devices": "38/42"
        }
    }

# ===== DASHBOARD =====
st.set_page_config(layout="wide")
data = get_data()

# Sidebar
with st.sidebar:
    st.title("Safebloq")
    st.selectbox("View", ["Dashboard", "Reports"])

# Main Content
st.title("Security Dashboard")

# KPIs
col1, col2 = st.columns(2)
col1.metric("Active Threats", data["kpis"]["active_threats"])
col2.metric("Secured Devices", data["kpis"]["secured_devices"])

# Threat Table
st.subheader("Recent Alerts")
st.dataframe(data["threats"])

# Simple Chart
st.subheader("Activity Trend")
chart_data = pd.DataFrame({"Day": [1, 2, 3], "Alerts": [3, 5, 2]})
st.bar_chart(chart_data, x="Day", y="Alerts")
