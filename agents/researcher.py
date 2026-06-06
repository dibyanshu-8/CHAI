import os
from langchain_tavily import TavilySearch

def researcher_node(state):
    """
    "Researcher node that fetches real-time news from the internet."
    """
    supplier = state["supplier_info"]
    
    # Specific query for supply chain intelligence
    query = f"latest supply chain disruptions, weather alerts, labor strikes, and logistics news for {supplier['city']} {supplier['country']}"
    
    print(f"DEBUG: Searching live web data for {supplier['supplier_name']}...")
    
    real_news = []
    
    # Get Tavily API key from environment
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if tavily_api_key:
        try:
            # Initialize Tavily search with explicit API key
            search = TavilySearch(tavily_api_key=tavily_api_key, max_results=5)
            search_results = search.invoke(query)
            real_news = [res['content'] for res in search_results]
            print(f"DEBUG: Retrieved {len(real_news)} results from Tavily")
        except Exception as e:
            print(f"Search failed for {supplier['supplier_name']}: {e}")
            real_news = [f"Automated monitoring active for {supplier['city']} region. No live alerts found."]
    else:
        print(f"Warning: TAVILY_API_KEY not set. Skipping live web search for {supplier['supplier_name']}.")
        real_news = [f"Automated monitoring active for {supplier['city']} region. No live alerts found."]

    return {
        "raw_news": real_news,
        "logs": [f"Researcher: Internet se {len(real_news)} live intelligence signals fetch kiye."]
    }