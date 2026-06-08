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
st.set_page_config(page_title="CHAI 2.0 | Cognitive Hazard AI", layout="wide")

# --- Load Supplier Data ---
@st.cache_data
def load_suppliers():
    # Make sure this path matches your directory structure
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
    st.header("⚙️ Settings")
    
    # THE MAGIC TOGGLE
    ai_mode = st.radio(
        "Select AI Architecture:",
        ("v2: Agentic AI (Live Data & Reasoning)", "v1: Classic RAG (Static CSV Data)")
    )
    
    st.divider()
    
    # Supplier Selection
    st.subheader("Target Supplier")
    supplier_names = suppliers_df['supplier_name'].tolist()
    selected_supplier_name = st.selectbox("Select Supplier:", supplier_names)
    
    # Get details of selected supplier
    supplier_info = suppliers_df[suppliers_df['supplier_name'] == selected_supplier_name].iloc[0].to_dict()
    
    st.write("**Location:**", f"{supplier_info['city']}, {supplier_info['country']}")
    st.write("**Products:**", supplier_info['products'])

# --- Main Interface ---
st.subheader(f"Risk Assessment: {supplier_info['supplier_name']}")

# Custom query input for Classic RAG, automated for Agentic
if "v1" in ai_mode:
    st.info("💡 **Classic RAG Mode:** Searching through historical static vector database (FAISS).")
    user_query = st.text_input("Enter your query:", f"Are there any risks for {supplier_info['supplier_name']}?")
    
    if st.button("Run Classic RAG Scan"):
        with st.spinner("Querying local vector database..."):
            response = ask_classic_rag(
                query=user_query, 
                supplier_name=supplier_info['supplier_name'], 
                location=f"{supplier_info['city']}, {supplier_info['country']}"
            )
            st.success("Scan Complete!")
            st.write(response)

else:
    st.success("🧠 **Agentic Mode:** Triggering multi-agent workflow with live Tavily search and Groq Llama 3.3.")
    
    if st.button("Run Live Agentic Scan"):
        with st.spinner("Agents are researching and analyzing live global data..."):
            try:
                # Initialize Graph
                app_graph = create_graph()
                
                # Setup initial state
                initial_state = {
                    "raw_news": [],
                    "supplier_info": supplier_info,
                    "identified_risks": [],
                    "final_alert": "",
                    "logs": []
                }
                
                # Run the graph
                final_state = app_graph.invoke(initial_state)
                
                # Display Results
                st.subheader("🚨 Final Intelligence Report")
                st.text(final_state.get("final_alert", "No report generated."))
                
                # Display internal thought process (Logs)
                with st.expander("View Agent Internal Logs"):
                    for log in final_state.get("logs", []):
                        st.write(f"- {log}")
                        
            except Exception as e:
                st.error(f"Agentic Pipeline Error: {e}")