import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load Environment Variables (Groq & Tavily API Keys)
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

# Import our two powerful engines
from core.v1_rag.basic_retriever import ask_classic_rag
from core.v2_agentic.graph import create_graph

# --- Page Config ---
st.set_page_config(page_title="Cognitive Hazard AI (CHAI)", layout="wide")


# App OFF = True , ON = False.
APP_OFFLINE = False  

if APP_OFFLINE:
    st.warning("**CHAI is temporarily offline.**")
    st.stop() 

# --- Rate Limiter Initialization ---
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
MAX_SCANS_PER_SESSION = 2

# --- Load Supplier Data ---
@st.cache_data
def load_suppliers():
    return pd.read_csv("core/shared_data/suppliers.csv")

try:
    suppliers_df = load_suppliers()
except Exception as e:
    st.error(f"Error loading suppliers.csv: {e}")
    st.stop()

# --- UI Header ---
st.title("Cognitive Hazard AI")
st.markdown("Monitor global supply chain disruptions using AI. Switch between Classic RAG and Agentic Reasoning.")

# --- Sidebar: Configuration & Toggle ---
with st.sidebar:
    st.header("Settings")
    
    ai_mode = st.radio(
        "Select AI Architecture:",
        ("v2: Agentic AI (Live Data & Reasoning)", "v1: Classic RAG (Static CSV Data)")
    )
    
    st.divider()
    
    st.subheader("Target Supplier")
    supplier_names = suppliers_df['supplier_name'].tolist()
    selected_supplier_name = st.selectbox("Select Supplier:", supplier_names)
    
    supplier_info = suppliers_df[suppliers_df['supplier_name'] == selected_supplier_name].iloc[0].to_dict()
    
    st.write("**Location:**", f"{supplier_info['city']}, {supplier_info['country']}")
    st.write("**Products:**", supplier_info['products'])

# --- Main Interface ---
st.subheader(f"Risk Assessment: {supplier_info['supplier_name']}")

# Custom query input for Classic RAG, automated for Agentic
if "v1" in ai_mode:
    st.info("**Classic RAG Mode:** Searching through historical static vector database (FAISS).")
    user_query = st.text_input("Enter your query:", f"Are there any risks for {supplier_info['supplier_name']}?")
    
    if st.button("Run Classic RAG Scan"):
        if st.session_state.scan_count >= MAX_SCANS_PER_SESSION:
            st.error("Limit exceeded! Refresh the page to start a new session.")
        else:
            with st.spinner("Querying local vector database..."):
                response = ask_classic_rag(
                    query=user_query, 
                    supplier_name=supplier_info['supplier_name'], 
                    location=f"{supplier_info['city']}, {supplier_info['country']}"
                )
                st.session_state.scan_count += 1
                st.success(f"Scan Complete! ({MAX_SCANS_PER_SESSION - st.session_state.scan_count} scans remaining)")
                st.write(response)

else:
    st.success("**Agentic Mode:** Triggering multi-agent workflow with live Tavily search and Groq Llama 3.3.")
    
    if st.button("Run Live Agentic Scan"):
        if st.session_state.scan_count >= MAX_SCANS_PER_SESSION:
            st.error("Limit exceeded! Refresh the page to start a new session.")
        else:
            with st.spinner("Agents are researching and analyzing live global data..."):
                try:
                    app_graph = create_graph()
                    
                    initial_state = {
                        "raw_news": [],
                        "supplier_info": supplier_info,
                        "identified_risks": [],
                        "final_alert": "",
                        "logs": []
                    }
                    
                    final_state = app_graph.invoke(initial_state)
                    
                    st.session_state.scan_count += 1
                    
                    st.subheader("Final Intelligence Report")
                    st.text(final_state.get("final_alert", "No report generated."))
                    
                    with st.expander("View Agent Internal Logs"):
                        for log in final_state.get("logs", []):
                            st.write(f"- {log}")
                            
                except Exception as e:
                    st.error(f"Agentic Pipeline Error: {e}")

# --- Professional Footer ---
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: #888888;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
.footer a {
    color: #4CAF50;
    text-decoration: none;
    font-weight: bold;
}
</style>
<div class="footer">
    <p>Built with 🧠 by <b>Dibyanshu</b> 
    <br>
    <a href="https://github.com/dibyanshu-8" target="_blank">GitHub</a> | 
    <a href="https://www.linkedin.com/in/dibyanshukar/" target="_blank">LinkedIn</a>
    </p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)