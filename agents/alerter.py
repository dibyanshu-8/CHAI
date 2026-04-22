#for formatting the final alert

from state import AgentState


def alerter_node(state: AgentState):
    risks = state.get("identified_risks", [])
    if state.get("final_alert") == "NO_RISK":
        return {"final_alert": "No alert needed."}
        
    supplier = state["supplier_info"]
    
    report = f"🚨 URGENT ALERT: {supplier['supplier_name']}\n"
    for r in risks:
        report += f"- {r['impact']} (Severity: {r['severity']})\n"
    
    return {
        "final_alert": report,
        "logs": ["Alerter formatted the final report."]
    }