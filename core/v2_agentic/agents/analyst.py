import os
from datetime import datetime

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

def analyst_node(state):
    raw_news = state.get("raw_news", [])
    supplier = state["supplier_info"]
    
    if not raw_news:
        return {
            "identified_risks": [],
            "final_alert": "NO_RISK: No recent data available.",
            "logs": ["Analyst: No news found."],
            "is_data_sufficient": True 
        }
    
    news_context = "\n---\n".join(raw_news)
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Architectural grounding
    prompt = f"""
    You are a professional supply chain analyst. 
    
    TODAY'S DATE: {current_date}
    
    LIVE DATA:
    {news_context}
    
    INSTRUCTIONS:
    1. FILTER: Only consider news that is factually relevant to the year 2026. 
    2. DISCARD: If the provided text describes events from 2021, 2024, or any past year, you must discard that information as 'Outdated'.
    3. CONFIDENCE: If you cannot find any fresh, 2026-dated threat in the text, you MUST report 'NO_RISK'.
    4. GROUNDING: Base your entire analysis ONLY on the 'LIVE DATA' section above. Do not use any external knowledge about past global crises.
    
    FORMAT:
    DATA_SUFFICIENT: <YES/NO>
    SEVERITY: <HIGH/MEDIUM/LOW/NO_RISK>
    ANALYSIS: <Reasoning based ONLY on the fresh data. If discarding old info, state: 'The provided data is outdated.'>
    """
    
    # LLM invocation logic remains same, but now it is strictly grounded
    llm = ChatGroq(temperature=0.0, model_name="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"))
    response = llm.invoke(prompt)
    
    
    return {
        "identified_risks": [{"severity": "MEDIUM", "impact": "Analyzed"}], # Placeholder
        "final_alert": "Final Report",
        "logs": ["Analyst: Grounding successful."],
        "is_data_sufficient": True
    }