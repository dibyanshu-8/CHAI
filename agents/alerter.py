def alerter_node(state):
    """
    This node takes the analysis from the Analyst and formats it into a 
    professional, high-impact report.
    """
    # Check if the Analyst marked this as No Risk
    if state.get("final_alert") == "NO_RISK":
        return {"final_alert": "SCAN COMPLETE: No immediate risks identified for this supplier."}
        
    risks = state.get("identified_risks", [])
    supplier = state["supplier_info"]
    
    # Building a professional, info-based report string
    report = f"\n [URGENT RISK ALERT] {supplier['supplier_name']}\n"
    report += "="*65 + "\n"
    report += f"LOCATION: {supplier['city']}, {supplier['country']}\n"
    report += f"PRODUCTS: {supplier['products']}\n"
    report += "="*65 + "\n"
    
    if not risks:
        report += "INFO: News events were detected near this location, but no direct supply chain impact was calculated by the AI.\n"
    else:
        # Loop through each risk identified by the Analyst
        for i, r in enumerate(risks, 1):
            impact = r.get('impact', 'N/A')
            severity = r.get('severity', 'N/A')
            
            # Select a symbol based on severity level (ASCII for Windows compatibility)
            sev_upper = severity.upper()
            if "HIGH" in sev_upper or "CRITICAL" in sev_upper:
                symbol = "[HIGH]"
            elif "MEDIUM" in sev_upper:
                symbol = "[MED]"
            else:
                symbol = "[LOW]"
            
            report += f"{i}. {symbol} SEVERITY: {sev_upper}\n"
            report += f"   IMPACT: {impact}\n"
            report += "-"*40 + "\n"
            
    report += "STRATEGIC RECOMMENDATION: Logistics team should verify ground status and assess alternative routing.\n"
    report += "="*65 + "\n"
    
    return {
        "final_alert": report,
        "logs": ["Alerter: Final detailed report generated successfully."]
    }