import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# ========================================
# Dependency Fix (Critical for Streamlit Cloud)
# ========================================
import sys
import subprocess

REQUIRED_PACKAGES = ["plotly==5.18.0", "pandas==2.1.4", "numpy==1.26.0"]
for package in REQUIRED_PACKAGES:
    try:
        __import__(package.split("==")[0])
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# ========================================
# Mock Data Generation
# ========================================
def generate_data():
    # Threat data
    threats = pd.DataFrame({
        "Time": [datetime.now() - timedelta(minutes=x) for x in [5, 15, 120]],
        "Type": ["Phishing", "Malware", "Brute Force"],
        "Severity": ["High", "Critical", "Medium"],
        "Device": ["Workstation-12", "Server-03", "Workstation-05"]
    })
    
    # KPIs
    kpis = {
        "active_threats": 3,
        "devices_secured": "38/42",
        "ziti_score": 84
    }
    
    # Charts
    fig = px.line(
        x=[1, 2, 3], 
        y=[3, 1, 6],
        title="Threat Trend",
        labels={"x": "Days", "y": "Alerts"}
    )
    
    return {"threats": threats, "kpis": kpis, "chart": fig}

# ========================================
# Dashboard UI
# ========================================
st.set_page_config(
    page_title="Safebloq",
    layout="wide",
    page_icon="🛡️"
)

data = generate_data()

# ---- Sidebar ----
with st.sidebar:
    st.title("Safebloq")
    st.selectbox("Client", ["All", "Client A", "Client B"])
    st.button("Refresh Data")

# ---- Main Dashboard ----
st.title("Zero Trust Dashboard")

# KPI Row
col1, col2, col3 = st.columns(3)
col1.metric("Active Threats", data["kpis"]["active_threats"])
col2.metric("Secured Devices", data["kpis"]["devices_secured"])
col3.metric("Ziti Score", data["kpis"]["ziti_score"])

# Threat Table
st.subheader("Recent Threats")
st.dataframe(data["threats"], hide_index=True)

# Chart
st.subheader("Threat Trend")
st.plotly_chart(data["chart"], use_container_width=True)
