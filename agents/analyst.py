from utils.memory import is_duplicate_alert, save_to_memory
from langchain_groq import ChatGroq  
import os
import json

def analyst_node(state):
    news = state["raw_news"]
    supplier = state["supplier_info"] 
    
    #Memory Check
    if is_duplicate_alert(news):
        return {
            "final_alert": "NO_RISK", 
            "logs": [f"Memory: News for {supplier['supplier_name']} matches a recent alert. Skipping to avoid spam."]
        }
    
    #Empty News ChecK
    if not news:
        return {
            "final_alert": "NO_RISK", 
            "logs": ["Analyst: No relevant news found in this cycle."]
        }

    # Groq Model initialization
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""
    You are a Senior Supply Chain Risk Analyst for Myntra. 
    Analyze the following intelligence for supplier: {supplier['supplier_name']} in {supplier['city']}, {supplier['country']}.
    
    News Items found for this location: {news}
    
    Task:
    1. Perform causal reasoning: If this news is true, exactly how does it impact production, labor, or logistics?
    2. Be specific about potential delays or quality issues.
    
    Return ONLY a valid JSON list of objects.
    Format: [
      {{"impact": "Detailed explanation of the causal risk", "severity": "High/Medium/Low"}}
    ]
    """
    
    try:
        response = llm.invoke(prompt)
        content = response.content.strip().replace("```json", "").replace("```", "")
        risks = json.loads(content)
        
        save_to_memory(news)
        
    except Exception as e:
        
        risks = [{"impact": f"Risk detected but analysis encountered an error. News context: {news[0][:100]}...", "severity": "Medium"}]

    return {
        "identified_risks": risks,
        "logs": ["Analyst: Groq Llama 3.3 has completed causal reasoning and the memory has been updated."]
    }