import os
from datetime import datetime

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

def analyst_node(state):
    """
    Analyst node equipped with a Digital Clock to reject outdated historical hallucinations.
    """
    raw_news = state.get("raw_news", [])
    supplier = state["supplier_info"]
    
    
    if not raw_news:
        return {
            "identified_risks": [],
            "final_alert": "NO_RISK: No recent disruption vectors identified for this region.",
            "logs": [f"Analyst: No active news signals found for {supplier['supplier_name']}."],
            "is_data_sufficient": True 
        }
    
    news_context = "\n---\n".join(raw_news)
    
    #current data ingestion
    current_date = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().year
    
    prompt = f"""
    You are an expert supply chain risk analyst. Evaluate the following live intelligence signals.
    
    [SYSTEM CLOCK: TODAY IS {current_date}]
    You MUST evaluate all risks relative to this exact date.
    
    SUPPLIER INFO:
    Name: {supplier['supplier_name']}
    Location: {supplier['city']}, {supplier['country']}
    Products: {supplier['products']}
    
    LIVE INTELLIGENCE SIGNALS:
    {news_context}
    
    CRITICAL TEMPORAL INSTRUCTIONS (DO NOT IGNORE):
    1. Temporal Blindness Check: If the news describes historical events (e.g., 2021 COVID lockdowns, past strikes from previous years), IGNORE THEM.
    2. If all signals are clearly outdated and do not actively disrupt operations in {current_year}, you MUST classify the risk as NO_RISK.
    3. Are these signals RECENT and sufficient to make a confident supply chain risk assessment for {current_date}? If the news is outdated or irrelevant, say NO for DATA_SUFFICIENT.
    
    You must respond EXACTLY in the following format so the parser can read it. Do not include any extra introductory text.
    DATA_SUFFICIENT: <YES or NO>
    SEVERITY: <Choose only one: HIGH, MEDIUM, LOW, or NO_RISK>
    ANALYSIS: <Write a concise causal reasoning explaining the impact. If rejecting old data, explicitly state "Data is outdated historical context.">
    """
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    severity = "MEDIUM" 
    analysis_text = "Risk detected but analysis encountered an error."
    is_data_sufficient = True 
    
    if groq_api_key and ChatGroq:
        try:
            llm = ChatGroq(temperature=0.0, model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
            response = llm.invoke(prompt)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            
            current_key = None
            analysis_lines = []
            
            for line in response_content.split("\n"):
                line_upper = line.upper().strip()
                
                if line_upper.startswith("DATA_SUFFICIENT:"):
                    is_data_sufficient = "YES" in line_upper
                    current_key = "DATA_SUFFICIENT"
                elif line_upper.startswith("SEVERITY:"):
                    sev_val = line.split(":", 1)[1].strip().upper()
                    for s in ["HIGH", "MEDIUM", "LOW", "NO_RISK"]:
                        if s in sev_val:
                            severity = s
                            break
                    current_key = "SEVERITY"
                elif line_upper.startswith("ANALYSIS:"):
                    analysis_lines.append(line.split(":", 1)[1].strip())
                    current_key = "ANALYSIS"
                elif current_key == "ANALYSIS" and line.strip():
                    
                    analysis_lines.append(line.strip())
            
            if analysis_lines:
                analysis_text = " ".join(analysis_lines)
                
            
            if not any(s in severity for s in ["HIGH", "MEDIUM", "LOW", "NO_RISK"]):
                severity = "MEDIUM"
                
        except Exception as e:
            print(f"Groq Inference or Parsing failed for {supplier['supplier_name']}: {e}")
            analysis_text = f"Inference pipeline bypass active. News sample: {raw_news[0][:80]}..."
    else:
        print("Warning: GROQ_API_KEY not configured or library missing.")
        analysis_text = f"System offline fallback. Raw content preview: {raw_news[0][:80]}..."

    return {
        "identified_risks": [{"severity": severity, "impact": analysis_text}],
        "final_alert": f"SEVERITY: {severity}\nIMPACT: {analysis_text}",
        "logs": [f"Analyst (Time-Aware): Data Sufficient = {is_data_sufficient}. Checked against current date: {current_date}."],
        "is_data_sufficient": is_data_sufficient
    }