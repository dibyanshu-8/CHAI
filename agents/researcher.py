#for fetching & filtering news
import pandas as pd

from state import AgentState

def researcher_node(state:AgentState):
    supplier = state["supplier_info"]
    
    simulated_news = [
        "Cyclone alert in Bay of Bengal affecting Dhaka ports",
        "New labor strike announced in Ho Chi Minh City garment district",
        "Guangzhou customs implementing new 48-hour inspection delay",
        "Surat highway expansion completed",
        "Global container prices rise by 15%"
    ]
    
    relevant = [news for news in simulated_news if any(tag.lower() in news.lower() for tag in supplier['location_tags'].split())]
    
    return {
        "raw_news": relevant,
        "logs": [f"Researcher found {len(relevant)} relevant news items for {supplier['supplier_name']}."]
    }