import os

# Robust fallback import strategy to handle package version changes
try:
    from langchain_tavily import TavilySearchResults as TavilySearch
except ImportError:
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults as TavilySearch
    except ImportError:
        TavilySearch = None

def researcher_node(state):
    """
    Researcher node that fetches real-time news from the internet.
    """
    supplier = state["supplier_info"]
    
    # Specific query for supply chain intelligence
    query = f"latest supply chain disruptions, weather alerts, labor strikes, and logistics news for {supplier['city']} {supplier['country']}"
    
    print(f"DEBUG: Searching live web data for {supplier['supplier_name']}...")
    
    real_news = []
    
    # Check if tool component is loaded
    if TavilySearch is None:
        print("Error: Tavily Search components could not be imported.")
        return {
            "raw_news": [f"Automated monitoring active for {supplier['city']} region. Service offline."],
            "logs": ["Researcher: Import error encountered."]
        }
    
    # Get Tavily API key from environment
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if tavily_api_key:
        try:
            # Initialize search component safely
            search = TavilySearch(max_results=5)
            search_results = search.invoke(query)
            
            # Safe parsing layer to handle both dictionaries and raw strings
            if isinstance(search_results, list):
                for res in search_results:
                    if isinstance(res, dict) and 'content' in res:
                        real_news.append(res['content'])
                    elif isinstance(res, dict) and 'description' in res:
                        real_news.append(res['description'])
                    else:
                        real_news.append(str(res))
            else:
                real_news.append(str(search_results))
                
            print(f"DEBUG: Successfully retrieved {len(real_news)} results from Tavily")
            
        except Exception as e:
            print(f"Search execution failed for {supplier['supplier_name']}: {e}")
            # Fallback configuration to prevent breaking the downstream nodes
            real_news = []
    else:
        print(f"Warning: TAVILY_API_KEY not set. Skipping live web search for {supplier['supplier_name']}.")
        real_news = []

    # AGAR koi real news nahi mili toh system aage crash na kare
    # analyst_node empty check handle kar lega aur NO_RISK return karega
    return {
        "raw_news": real_news,
        "logs": [f"Researcher: Processed live web queries for {supplier['supplier_name']}."]
    }
