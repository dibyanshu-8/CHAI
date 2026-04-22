from langchain_groq import ChatGroq  # type: ignore
import os
import json

def analyst_node(state):
    news = state["raw_news"]
    supplier = state["supplier_info"]
    
    # Agar news empty hai toh aage nahi badhna
    if not news:
        return {"final_alert": "NO_RISK", "logs": ["Analyst: Koi relevant news nahi mili."]}

    # Latest Groq Model use kar rahe hain
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
        # Markdown clean karna
        content = response.content.strip().replace("```json", "").replace("```", "")
        risks = json.loads(content)
    except Exception as e:
        # Fallback agar AI response format galat ho
        risks = [{"impact": f"Analysis partially failed but news was detected. Context: {news[0]}", "severity": "Medium"}]

    return {
        "identified_risks": risks,
        "logs": ["Analyst: Groq Llama 3.3 ne causal reasoning complete kar li hai."]
    }