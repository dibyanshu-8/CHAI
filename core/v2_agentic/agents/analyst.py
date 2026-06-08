import os
import json
# Jin frameworks ko aap deploy kar rahe ho unke standard imports
try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

def analyst_node(state):
    """
    Analyst node jo Tavily ke live data par Groq use karke causal reasoning apply karta hai.
    """
    raw_news = state.get("raw_news", [])
    supplier = state["supplier_info"]
    
    # Agar koi news hi nahi mili, toh calculation skip karke NO_RISK set karo
    if not raw_news:
        return {
            "identified_risks": [],
            "final_alert": "NO_RISK: No recent disruption vectors identified for this region.",
            "logs": [f"Analyst: No active news signals found for {supplier['supplier_name']}."]
        }
    
    # Combined context create karein
    news_context = "\n---\n".join(raw_news)
    
    # Strict prompt for Groq to prevent fallback errors
    prompt = f"""
    You are an expert supply chain risk analyst. Analyze the following live intelligence signals for a supplier and evaluate the risk severity.
    
    SUPPLIER INFO:
    Name: {supplier['supplier_name']}
    Location: {supplier['city']}, {supplier['country']}
    Products: {supplier['products']}
    
    LIVE INTELLIGENCE SIGNALS:
    {news_context}
    
    CRITICAL INSTRUCTION: You must respond in the following format so the parser can read it. Do not include any extra introductory text.
    SEVERITY: <Choose only one: HIGH, MEDIUM, LOW, or NO_RISK>
    ANALYSIS: <Write a concise 2-sentence causal reasoning explaining the direct impact on production or logistics>
    """
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    severity = "HIGH" # Fallback default
    analysis_text = "Risk detected but analysis encountered an error."
    
    if groq_api_key and ChatGroq:
        try:
            # High-speed LPU routing configuration
            llm = ChatGroq(temperature=0.1, model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
            response = llm.invoke(prompt)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Smart parsing layer: text line by line scan karenge taaki custom fields extract ho sakein
            lines = response_content.split("\n")
            for line in lines:
                if line.upper().startswith("SEVERITY:"):
                    severity = line.split(":", 1)[1].strip().upper()
                if line.upper().startswith("ANALYSIS:"):
                    analysis_text = line.split(":", 1)[1].strip()
            
            # Edge-case safety: Ensure severity matches standard strings
            if not any(s in severity for s in ["HIGH", "MEDIUM", "LOW", "NO_RISK"]):
                severity = "MEDIUM"
                
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
        "logs": [f"Analyst: Groq Llama 3.3 completed causal reasoning for {supplier['supplier_name']}."]
    }
