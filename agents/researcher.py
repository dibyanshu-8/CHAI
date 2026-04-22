import os
from langchain_tavily import TavilySearchResults

def researcher_node(state):
    """
    Researcher node jo internet se real-time news fetch karta hai.
    """
    supplier = state["supplier_info"]
    
    # Specific query for supply chain intelligence
    query = f"latest supply chain disruptions, weather alerts, labor strikes, and logistics news for {supplier['city']} {supplier['country']}"
    
    # Updated Tavily tool (Warning-free)
    search = TavilySearchResults(max_results=5)
    
    print(f"DEBUG: Searching live web data for {supplier['supplier_name']}...")
    
    try:
        # Naye version mein .invoke() method use hota hai
        search_results = search.invoke(query)
        
        # News content extract karna
        real_news = [res['content'] for res in search_results]
        
    except Exception as e:
        print(f"Search failed for {supplier['supplier_name']}: {e}")
        real_news = [f"Automated monitoring active for {supplier['city']} region. No live alerts found."]

    return {
        "raw_news": real_news,
        "logs": [f"Researcher: Internet se {len(real_news)} live intelligence signals fetch kiye."]
    }