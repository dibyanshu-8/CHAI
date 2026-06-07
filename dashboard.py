"""
CHAI 2.0 - Responsive UI Dashboard
Modern, interactive dashboard for Cognitive Hazard AI supply chain monitoring
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import random
from dotenv import load_dotenv

# Load environment
load_dotenv(override=True)

# Page configuration
st.set_page_config(
    page_title="CHAI 2.0 - Supply Chain Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --success-color: #2ca02c;
        --danger-color: #d62728;
        --warning-color: #ff7f0e;
        --info-color: #17becf;
    }
    
    /* Responsive containers */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .alert-high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-left: 4px solid #f5576c;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #ffa751 0%, #ffe259 100%);
        border-left: 4px solid #ffe259;
    }
    
    .alert-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-left: 4px solid #00f2fe;
    }
    
    .supplier-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        transition: all 0.3s;
    }
    
    .supplier-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    
    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    
    .status-active { background-color: #d4edda; color: #155724; }
    .status-risk { background-color: #f8d7da; color: #721c24; }
    .status-critical { background-color: #f5c6cb; color: #721c24; }
    
    /* Sidebar styling */
    .sidebar-section {
        margin-bottom: 20px;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Header styling */
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* Data table styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    
    .dataframe th {
        background-color: #667eea;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    
    .dataframe td {
        padding: 10px 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .dataframe tr:hover {
        background-color: #f5f5f5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            padding: 15px;
        }
        .header-title {
            font-size: 1.8em;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'suppliers_data' not in st.session_state:
    st.session_state.suppliers_data = None
if 'alerts_history' not in st.session_state:
    st.session_state.alerts_history = []

# ============= UTILITY FUNCTIONS =============

@st.cache_data
def load_suppliers_data():
    """Load suppliers data from CSV"""
    try:
        suppliers_df = pd.read_csv("suppliers.csv")
        return suppliers_df
    except FileNotFoundError:
        return pd.DataFrame({
            'supplier_name': ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D'],
            'region': ['China', 'Vietnam', 'India', 'Taiwan'],
            'category': ['Electronics', 'Manufacturing', 'Logistics', 'Electronics'],
            'risk_level': ['High', 'Low', 'Medium', 'High']
        })

@st.cache_data
def load_events_data():
    """Load global events data"""
    try:
        events_df = pd.read_csv("global_events.csv")
        return events_df
    except FileNotFoundError:
        return pd.DataFrame()

def generate_risk_score(risk_level):
    """Generate numeric risk score based on level"""
    scores = {'Low': 25, 'Medium': 50, 'High': 75, 'Critical': 100}
    return scores.get(risk_level, 50)

def get_alert_color(severity):
    """Get color based on alert severity"""
    colors = {
        'High': '#f5576c',
        'Medium': '#ffe259',
        'Low': '#00f2fe',
        'Critical': '#ff0000'
    }
    return colors.get(severity, '#667eea')

def create_mock_alerts():
    """Create mock alerts for demonstration"""
    alerts = [
        {
            'id': 'ALT-001',
            'supplier': 'Supplier A',
            'severity': 'High',
            'title': 'Geopolitical Tensions in Manufacturing Hub',
            'description': 'Rising tensions detected in primary production region.',
            'timestamp': datetime.now() - timedelta(hours=2),
            'mitigation': 'Diversify supply sources'
        },
        {
            'id': 'ALT-002',
            'supplier': 'Supplier B',
            'severity': 'Medium',
            'title': 'Weather Disruption Expected',
            'description': 'Typhoon approaching manufacturing facility.',
            'timestamp': datetime.now() - timedelta(hours=5),
            'mitigation': 'Accelerate shipments before impact'
        },
        {
            'id': 'ALT-003',
            'supplier': 'Supplier C',
            'severity': 'Low',
            'title': 'Labor Negotiations Update',
            'description': 'Routine labor negotiations ongoing.',
            'timestamp': datetime.now() - timedelta(hours=12),
            'mitigation': 'Monitor negotiations progress'
        }
    ]
    return alerts

# ============= HEADER SECTION =============

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h1 class="header-title">🚀 CHAI 2.0 Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Cognitive Hazard AI - Real-time Supply Chain Intelligence**")

with col2:
    st.metric("Last Update", datetime.now().strftime("%H:%M:%S"), delta="Just now")

st.divider()

# ============= SIDEBAR =============

with st.sidebar:
    st.markdown("### ⚙️ Dashboard Settings")
    
    # Filters
    st.markdown("**Filters**")
    severity_filter = st.multiselect(
        "Alert Severity",
        ["High", "Medium", "Low", "Critical"],
        default=["High", "Medium", "Low", "Critical"]
    )
    
    region_filter = st.multiselect(
        "Regions",
        ["All Regions", "Asia", "Europe", "Americas", "Africa"],
        default=["All Regions"]
    )
    
    # Refresh settings
    st.markdown("**Auto Refresh**")
    refresh_interval = st.select_slider(
        "Refresh interval (minutes)",
        options=[1, 5, 10, 30, 60],
        value=5
    )
    
    # Display settings
    st.markdown("**Display**")
    view_mode = st.radio(
        "View Mode",
        ["Dashboard", "Analytics", "Alerts", "Suppliers"]
    )
    
    st.divider()
    st.markdown("**System Status**")
    st.info("✅ All agents active and monitoring")
    st.success(f"🔄 Auto-refresh every {refresh_interval}min")

# ============= MAIN CONTENT AREA =============

if view_mode == "Dashboard":
    # Load data
    suppliers_df = load_suppliers_data()
    alerts = create_mock_alerts()
    
    # Key Metrics Row
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Suppliers", len(suppliers_df), "+2", delta_color="inverse")
    
    with col2:
        high_risk = len(suppliers_df[suppliers_df['risk_level'] == 'High'])
        st.metric("High Risk", high_risk, "-1", delta_color="off")
    
    with col3:
        total_alerts = len(alerts)
        st.metric("Active Alerts", total_alerts, "+1")
    
    with col4:
        st.metric("System Health", "98%", "+2%", delta_color="off")
    
    st.divider()
    
    # Real-time Alerts Section
    st.markdown("### 🚨 Real-Time Alerts")
    
    filtered_alerts = [a for a in alerts if a['severity'] in severity_filter]
    
    for alert in filtered_alerts:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: {get_alert_color(alert['severity'])}33; padding: 15px; border-radius: 8px; border-left: 4px solid {get_alert_color(alert['severity'])};">
                    <b>{alert['title']}</b><br>
                    <small>{alert['description']}</small><br>
                    <span style="color: #666; font-size: 0.85em;">ID: {alert['id']} | {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                severity_color = get_alert_color(alert['severity'])
                st.markdown(f"""
                <span style="background-color: {severity_color}33; color: {severity_color}; padding: 8px 12px; border-radius: 20px; font-weight: bold;">
                    {alert['severity']}
                </span>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("View Details", key=alert['id']):
                    st.session_state.selected_alert = alert
                    st.rerun()
            
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Supplier Risk Map
    st.markdown("### 🗺️ Supplier Risk Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution pie chart
        risk_counts = suppliers_df['risk_level'].value_counts()
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Distribution",
            color_discrete_map={'High': '#f5576c', 'Medium': '#ffe259', 'Low': '#00f2fe'},
            hole=0.3
        )
        fig_pie.update_traces(marker=dict(line=dict(color='white', width=2)))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Risk by category bar chart
        if 'category' in suppliers_df.columns:
            risk_by_category = suppliers_df.groupby('category')['risk_level'].value_counts().unstack(fill_value=0)
            fig_bar = px.bar(
                risk_by_category,
                title="Risk by Category",
                barmode='group',
                color_discrete_map={'High': '#f5576c', 'Medium': '#ffe259', 'Low': '#00f2fe'}
            )
            fig_bar.update_layout(hovermode='x unified')
            st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    
    # Suppliers Table
    st.markdown("### 📋 Suppliers Database")
    
    if not suppliers_df.empty:
        # Create styled dataframe
        display_df = suppliers_df.copy()
        
        # Add status badges
        status_map = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        if 'risk_level' in display_df.columns:
            display_df['Status'] = display_df['risk_level'].map(lambda x: f"{status_map.get(x, '⚪')} {x}")
        
        st.dataframe(display_df, use_container_width=True, height=300)
        
        # Supplier details expander
        with st.expander("Detailed Supplier Information"):
            selected_supplier = st.selectbox(
                "Select Supplier",
                suppliers_df['supplier_name'].tolist() if 'supplier_name' in suppliers_df.columns else []
            )
            if selected_supplier:
                supplier_data = suppliers_df[suppliers_df['supplier_name'] == selected_supplier].iloc[0]
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info(f"**Region**: {supplier_data.get('region', 'N/A')}")
                with col2:
                    st.info(f"**Category**: {supplier_data.get('category', 'N/A')}")
                with col3:
                    st.warning(f"**Risk Level**: {supplier_data.get('risk_level', 'N/A')}")

elif view_mode == "Analytics":
    st.markdown("### 📈 Advanced Analytics")
    
    # Timeline analysis
    st.markdown("#### Alert Trends (Last 30 Days)")
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    alert_counts = [random.randint(2, 8) for _ in dates]
    
    df_timeline = pd.DataFrame({
        'Date': dates,
        'Alerts': alert_counts
    })
    
    fig_timeline = px.area(
        df_timeline,
        x='Date',
        y='Alerts',
        title="Alert Frequency Over Time",
        fill='tozeroy'
    )
    fig_timeline.update_traces(fillcolor='rgba(102, 126, 234, 0.2)', line=dict(color='#667eea'))
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Risk categories analysis
    st.markdown("#### Risk Category Breakdown")
    
    categories = ['Geopolitical', 'Weather', 'Labor', 'Logistics', 'Market', 'Supply']
    values = [15, 12, 8, 10, 7, 6]
    
    fig_cat = px.bar(
        x=categories,
        y=values,
        title="Alert Distribution by Category",
        labels={'x': 'Category', 'y': 'Number of Alerts'}
    )
    fig_cat.update_traces(marker_color='#667eea')
    st.plotly_chart(fig_cat, use_container_width=True)

elif view_mode == "Alerts":
    st.markdown("### 🚨 Alerts Management")
    
    alerts = create_mock_alerts()
    
    # Alert filters
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search alerts", "")
    with col2:
        sort_by = st.selectbox("Sort by", ["Latest", "Severity", "Supplier"])
    
    # Filter and display
    filtered_alerts = [a for a in alerts if search_term.lower() in a['title'].lower() or search_term.lower() in a['description'].lower()]
    
    if sort_by == "Severity":
        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        filtered_alerts.sort(key=lambda x: severity_order.get(x['severity'], 4))
    elif sort_by == "Latest":
        filtered_alerts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    for alert in filtered_alerts:
        with st.expander(f"**{alert['severity']}** - {alert['title']} ({alert['id']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Supplier**: {alert['supplier']}")
                st.markdown(f"**Description**: {alert['description']}")
                st.markdown(f"**Timestamp**: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Mitigation**: {alert['mitigation']}")
            
            with col2:
                st.button("📧 Send Alert", key=f"send_{alert['id']}")
                st.button("✅ Acknowledge", key=f"ack_{alert['id']}")
                st.button("🔖 Archive", key=f"arch_{alert['id']}")

elif view_mode == "Suppliers":
    st.markdown("### 📊 Supplier Management")
    
    suppliers_df = load_suppliers_data()
    
    # Add new supplier
    with st.expander("➕ Add New Supplier"):
        col1, col2 = st.columns(2)
        
        with col1:
            supplier_name = st.text_input("Supplier Name")
            region = st.selectbox("Region", ["Asia", "Europe", "Americas", "Africa"])
        
        with col2:
            category = st.selectbox("Category", ["Electronics", "Manufacturing", "Logistics", "Raw Materials"])
            risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
        
        if st.button("Add Supplier"):
            st.success(f"✅ Supplier '{supplier_name}' added successfully!")
    
    st.divider()
    
    # Supplier list
    st.markdown("#### All Suppliers")
    
    if not suppliers_df.empty:
        for idx, supplier in suppliers_df.iterrows():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{supplier.get('supplier_name', 'N/A')}**")
            with col2:
                st.markdown(f"*{supplier.get('region', 'N/A')}*")
            with col3:
                st.markdown(f"{supplier.get('category', 'N/A')}")
            with col4:
                risk = supplier.get('risk_level', 'N/A')
                color = get_alert_color(risk)
                st.markdown(f"<span style='color: {color}; font-weight: bold;'>{risk}</span>", unsafe_allow_html=True)
            
            st.divider()

# ============= FOOTER =============

st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.85em;'>
    <p>CHAI 2.0 Dashboard | Real-time Supply Chain Intelligence</p>
    <p>Powered by LangGraph, Groq, and Streamlit | © 2024</p>
</div>
""", unsafe_allow_html=True)
