import sys
import subprocess

# Auto-install critical dependencies
REQUIRED_PACKAGES = ["plotly==5.18.0", "pandas==2.1.4"]
for package in REQUIRED_PACKAGES:
    try:
        __import__(package.split("==")[0])
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import plotly
except ImportError:
    install("plotly==5.18.0")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ========================================
# Configuration
# ========================================
st.set_page_config(
    page_title="Safebloq - Zero Trust Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ========================================
# Mock Authentication
# ========================================
def authenticate():
    """Simple mock authentication for MVP"""
    return {
        "username": "admin",
        "tenant": "Demo MSP",
        "role": "admin"
    }

# ========================================
# Mock Data Generation
# ========================================
def generate_mock_data():
    """Generate all mock data for the dashboard"""
    # Threat feed data
    threats = pd.DataFrame({
        "Timestamp": [datetime.now() - timedelta(minutes=x) for x in [5, 32, 120, 240, 360]],
        "Threat Type": ["Phishing", "Ransomware", "Brute Force", "Malware", "Suspicious Login"],
        "Severity": ["High", "Critical", "Medium", "High", "Low"],
        "Source IP": [f"192.168.1.{np.random.randint(100)}" for _ in range(5)],
        "Status": ["Active", "Contained", "Investigating", "Contained", "Active"],
        "Device": [f"Device-{chr(65+i)}" for i in range(5)]
    })

    # Device compliance data
    device_status = pd.DataFrame({
        "Device": [f"Device-{chr(65+i)}" for i in range(10)],
        "Status": ["Compliant"]*7 + ["Non-Compliant"]*3,
        "Last Scanned": [datetime.now() - timedelta(hours=np.random.randint(1, 72)) for _ in range(10)]
    })

    # KPI data
    kpis = {
        "active_threats": 5,
        "phishing_attempts": 12,
        "devices_total": 42,
        "devices_unsafe": 7,
        "ziti_score": 82
    }

    # Charts
    threat_trend = px.line(
        x=pd.date_range(start="2024-06-01", periods=30, freq="D"),
        y=np.random.randint(1, 15, 30),
        title="Threat Trend (30 Days)",
        labels={"x": "Date", "y": "Threat Count"},
        color_discrete_sequence=["#FF4B4B"]
    )

    compliance_chart = px.pie(
        device_status,
        names="Status",
        title="Device Compliance",
        color_discrete_sequence=["#1DD1A1", "#FF6B6B"]
    )

    return {
        "threats": threats,
        "device_status": device_status,
        "kpis": kpis,
        "charts": {
            "threat_trend": threat_trend,
            "compliance": compliance_chart
        }
    }

# ========================================
# Dashboard UI
# ========================================
def main():
    # Authenticate user
    user = authenticate()
    if not user:
        st.error("Authentication failed")
        return

    # Load data
    data = generate_mock_data()

    # ===== SIDEBAR =====
    with st.sidebar:
        st.title("Safebloq")
        st.image("https://via.placeholder.com/150x50?text=Safebloq", width=150)
        
        st.selectbox("Select Client", ["All Clients", "Client A", "Client B", "Client C"])
        st.selectbox("Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
        
        st.divider()
        st.markdown(f"**Tenant:** {user['tenant']}")
        st.markdown(f"**User:** {user['username']} ({user['role']})")

    # ===== MAIN DASHBOARD =====
    st.title(f"Zero Trust Security Dashboard")
    
    # ---- KPIs ----
    cols = st.columns(4)
    cols[0].metric("Active Threats", data["kpis"]["active_threats"], "3 new", help="Currently active security threats")
    cols[1].metric("Phishing Attempts", data["kpis"]["phishing_attempts"], "2 today", help="Email/URL phishing attempts blocked")
    cols[2].metric("Devices at Risk", 
                  f"{data['kpis']['devices_unsafe']}/{data['kpis']['devices_total']}", 
                  "-2%", 
                  help="Devices with compliance violations")
    cols[3].metric("Zero Trust Score", 
                  f"{data['kpis']['ziti_score']}/100", 
                  "▲2", 
                  help="Overall security posture score")

    st.divider()

    # ---- Threat Section ----
    st.header("🛡️ Live Threat Feed")
    st.dataframe(
        data["threats"],
        column_config={
            "Timestamp": st.column_config.DatetimeColumn("Time"),
            "Severity": st.column_config.TextColumn("Severity", help="Threat severity level")
        },
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ---- Charts ----
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(data["charts"]["threat_trend"], use_container_width=True)
    with col2:
        st.plotly_chart(data["charts"]["compliance"], use_container_width=True)

    # ---- Device Status ----
    st.header("💻 Device Compliance")
    st.dataframe(
        data["device_status"],
        column_config={
            "Last Scanned": st.column_config.DatetimeColumn("Last Scanned"),
            "Status": st.column_config.TextColumn("Status", help="Compliance status")
        },
        use_container_width=True,
        hide_index=True
    )

# Run the app
if __name__ == "__main__":
    main()
