import os

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

def analyst_node(state):
    """
    Analyst node jo Tavily ke live data par Groq use karke causal reasoning apply karta hai
    aur decide karta hai ki data sufficient hai ya aur search ki zaroorat hai.
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
    
    # Combined context create karein
    news_context = "\n---\n".join(raw_news)
    
    # NEW PROMPT: Data sufficiency check enforced
    prompt = f"""
    You are an expert supply chain risk analyst. Evaluate the following live intelligence signals.
    
    SUPPLIER INFO:
    Name: {supplier['supplier_name']}
    Location: {supplier['city']}, {supplier['country']}
    Products: {supplier['products']}
    
    LIVE INTELLIGENCE SIGNALS:
    {news_context}
    
    CRITICAL INSTRUCTION: Analyze the signals. Are these signals highly relevant and sufficient to make a confident supply chain risk assessment? 
    If the news is irrelevant or too vague, say NO. If it is relevant and clear, say YES.
    
    You must respond EXACTLY in the following format. Do not include any extra introductory text.
    DATA_SUFFICIENT: <YES or NO>
    SEVERITY: <HIGH, MEDIUM, LOW, or NO_RISK>
    ANALYSIS: <Write your reasoning here>
    """
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    severity = "MEDIUM" 
    analysis_text = "Risk detected but analysis encountered an error."
    is_data_sufficient = True 
    
    if groq_api_key and ChatGroq:
        try:
            llm = ChatGroq(temperature=0.1, model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
            response = llm.invoke(prompt)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Robust parsing for multi-line LLM outputs
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
                    # Capture multi-line reasoning safely
                    analysis_lines.append(line.strip())
            
            if analysis_lines:
                analysis_text = " ".join(analysis_lines)
                
        except Exception as e:
            print(f"Groq Inference or Parsing failed for {supplier['supplier_name']}: {e}")
            analysis_text = f"Inference pipeline bypass active. News sample: {raw_news[0][:80]}..."
    else:
        print("Warning: GROQ_API_KEY not configured or library missing.")
        analysis_text = f"System offline fallback. Raw content preview: {raw_news[0][:80]}..."

    # State update package creation
    return {
        "identified_risks": [{"severity": severity, "impact": analysis_text}],
        "final_alert": f"SEVERITY: {severity}\nIMPACT: {analysis_text}",
        "logs": [f"Analyst: Data Sufficient = {is_data_sufficient}. Causal reasoning complete."],
        "is_data_sufficient": is_data_sufficient
    }