import os
from datetime import datetime


try:
    from langchain_tavily import TavilySearchResults as TavilySearch
except ImportError:
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults as TavilySearch
    except ImportError:
        TavilySearch = None

def researcher_node(state):
    """
    Researcher node with Temporal Grounding to bypass Search Authority Bias.
    """
    supplier = state["supplier_info"]
    current_attempt = state.get("search_count", 0) + 1 
    existing_news = state.get("raw_news", [])
    
    # Get real-time date constraints 
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    
    # Dynamic Query Routing with Time-Awareness
    if current_attempt == 1:
        query = f"latest supply chain disruptions, labor strikes, logistics news {supplier['city']} {supplier['country']} {current_month} {current_year}"
    else:
        query = f"recent active port congestion, hidden delays {supplier['city']} {supplier['country']} news {current_year}"
        
    print(f"DEBUG: Searching live web data for {supplier['supplier_name']}... (Attempt {current_attempt} | Timeframe: {current_year})")
    
    real_news = []
    
    # Check if tool component is loaded
    if TavilySearch is None:
        print("Error: Tavily Search components could not be imported.")
        return {
            "raw_news": existing_news + [f"Automated monitoring active for {supplier['city']} region. Service offline."],
            "logs": ["Researcher: Import error encountered."],
            "search_count": 1
        }
    
    # Get Tavily API key from environment
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if tavily_api_key:
        try:
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
    else:
        print(f"Warning: TAVILY_API_KEY not set. Skipping live web search.")

    # Combine old context with new context safely
    updated_news = existing_news + real_news

    return {
        "raw_news": updated_news,
        "logs": [f"Researcher: Processed time-aware web query (Attempt {current_attempt}). Fetched {len(real_news)} new items."],
        "search_count": 1  
    }