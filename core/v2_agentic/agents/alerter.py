def alerter_node(state):
    """
    This node takes the analysis from the Analyst and formats it into a 
    professional, high-impact Markdown report for the Streamlit UI.
    """
    final_alert_str = state.get("final_alert", "")
    risks = state.get("identified_risks", [])
    
    
    supplier = state.get("supplier_info", {})
    supplier_name = supplier.get('supplier_name', 'Unknown Supplier')
    supplier_city = supplier.get('city', 'Unknown City')
    supplier_country = supplier.get('country', 'Unknown Country')
    supplier_products = supplier.get('products', 'Unknown Products')
    
    
    if "NO_RISK" in final_alert_str or (risks and risks[0].get("severity", "") == "NO_RISK"):
        return {
            "final_alert": f"**SCAN COMPLETE:** No active or immediate supply chain disruption vectors identified for **{supplier_name}** at this time.",
            "logs": ["Alerter: Registered NO_RISK status. Formatted safe response."]
        }
        
    
    report = f"### URGENT RISK ALERT: {supplier_name}\n"
    report += "---\n"
    report += f"** LOCATION:** {supplier_city}, {supplier_country} \n\n"
    report += f"** PRODUCTS:** {supplier_products} \n"
    report += "---\n\n"
    
    if not risks:
        report += "*INFO: Intelligence signals were detected, but no direct supply chain impact was calculated by the AI.*\n\n"
    else:
        # Loop through each risk identified by the Analyst
        for i, r in enumerate(risks, 1):
            impact = r.get('impact', 'Analysis processing error.')
            severity = r.get('severity', 'MEDIUM')
            
            # Select an emoji based on severity level
            sev_upper = severity.upper()
            if "HIGH" in sev_upper or "CRITICAL" in sev_upper:
                emoji = "🔴"
            elif "MEDIUM" in sev_upper:
                emoji = "🟡"
            else:
                emoji = "🟢"
            
            
            report += f"#### {emoji} Risk {i}: {sev_upper} SEVERITY\n"
            report += f"> **IMPACT:** {impact}\n\n"
            
    report += "---\n"
    report += "💡 **STRATEGIC RECOMMENDATION:** *Logistics team should verify ground status and assess alternative routing.*"
    
    return {
        "final_alert": report,
        "logs": ["Alerter: Final markdown-optimized report generated successfully."]
    }