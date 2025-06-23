import sys
import subprocess

# ==================== DEPENDENCY INSTALLATION ====================
def ensure_packages():
    required = {
        "streamlit": "1.29.0",
        "pandas": "2.1.4",
        "plotly": "5.18.0",
        "numpy": "1.26.0"
    }
    for pkg, ver in required.items():
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg}=={ver}"])

ensure_packages()

# ==================== IMPORTS ====================
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# ==================== MOCK DATA ====================
def generate_data():
    threats = pd.DataFrame({
        "Time": [(datetime.now() - timedelta(minutes=x)).strftime("%Y-%m-%d %H:%M") for x in [5, 15, 120]],
        "Type": ["Phishing", "Malware", "Brute Force"],
        "Severity": ["High", "Critical", "Medium"],
        "Device": ["Workstation-12", "Server-03", "Workstation-05"]
    })
    
    kpis = {
        "active_threats": 3,
        "devices_secured": "38/42",
        "ziti_score": 84
    }
    
    fig = px.line(
        x=["Day 1", "Day 2", "Day 3"],  # Changed to strings for better labels
        y=[3, 1, 6],
        title="Threat Trend",
        labels={"x": "Timeline", "y": "Alerts"}
    )
    
    return {"threats": threats, "kpis": kpis, "chart": fig}

# ==================== DASHBOARD ====================
st.set_page_config(
    page_title="Safebloq",
    layout="wide",
    page_icon="🛡️"
)

data = generate_data()

# ---- Sidebar ----
with st.sidebar:
    st.title("Safebloq")
    st.selectbox("Client", ["All", "Client A", "Client B"], key="client_select")
    st.button("Refresh Data", key="refresh_btn")

# ---- Main Dashboard ----
st.title("Zero Trust Dashboard")

# KPI Row
col1, col2, col3 = st.columns(3)
col1.metric("Active Threats", data["kpis"]["active_threats"])
col2.metric("Secured Devices", data["kpis"]["devices_secured"])
col3.metric("Ziti Score", data["kpis"]["ziti_score"])

# Threat Table
st.subheader("Recent Threats")
st.dataframe(data["threats"], hide_index=True, use_container_width=True)

# Chart
st.subheader("Threat Trend")
st.plotly_chart(data["chart"], use_container_width=True)
