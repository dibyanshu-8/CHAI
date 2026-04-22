import os
from langchain_community.tools.tavily_search import TavilySearchResults 

def researcher_node(state):
    supplier = state["supplier_info"]
    query = f"latest supply chain news weather labor strike logistics in {supplier['city']} {supplier['country']}"
    
    # Initialize Tavily Search (Professional Search tool for Agents)
    # Iske liye 'pip install langchain-community' karna hoga
    search = TavilySearchResults(k=3) # Top 3 news results
    
    print(f"DEBUG: Searching real-time data for {supplier['supplier_name']}...")
    
    try:
        search_results = search.run(query)
        # News content ko extract karna
        real_news = [res['content'] for res in search_results]
    except Exception as e:
        print(f"Search failed, using fallback. Error: {e}")
        real_news = [f"General monitoring active for {supplier['city']} region."]

    return {
        "raw_news": real_news,
        "logs": [f"Researcher: Fetched {len(real_news)} live intelligence signals from web."]
    }