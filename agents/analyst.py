#for casual reasoning
import groq
import os
import json
from state import AgentState

# Configure Groq client
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

def analyst_node(state: AgentState):
    news = state["raw_news"]
    supplier = state["supplier_info"]

    if not news:
        return {
            "final_alert": "NO_RISK",
            "logs": ["Analyst found no significant news to act upon."]
        }

    prompt = f"""
    Analyze these news items for supplier {supplier['supplier_name']} in {supplier['city']}.
    News: {news}
    Perform causal reasoning. If this news is true, how does it hurt Myntra's supply?
    Return ONLY a JSON list of risks with 'impact' and 'severity'.
    """

    # Call Groq API
    response = client.chat.completions.create(
        model="llama3-70b-8192",   # Example Groq model
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract response text
    response_text = response.choices[0].message.content.strip()

    # Clean and parse JSON
    try:
        risks = json.loads(response_text.replace("```json", "").replace("```", "").strip())
    except:
        risks = [{"impact": "General disruption", "severity": "Medium"}]

    return {
        "identified risks": risks,
        "logs": ["Analyst completed causal reasoning."]
    }