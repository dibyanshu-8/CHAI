import os


try:
    from langchain_tavily import TavilySearchResults as TavilySearch
except ImportError:
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults as TavilySearch
    except ImportError:
        TavilySearch = None

def researcher_node(state):
    """
    Researcher node that fetches real-time news. If looping, it alters the query to find deeper context.
    """
    supplier = state["supplier_info"]
    current_attempt = state.get("search_count", 0) + 1 
    
    
    existing_news = state.get("raw_news", [])
    
    
    if current_attempt == 1:
        query = f"latest supply chain disruptions, weather alerts, labor strikes, and logistics news for {supplier['city']} {supplier['country']}"
    else:
        query = f"in-depth investigative news, hidden logistics delays, port congestion {supplier['city']} {supplier['country']} recent"
        
    print(f"DEBUG: Searching live web data for {supplier['supplier_name']}... (Attempt {current_attempt})")
    
    real_news = []
    
    if TavilySearch is None:
        print("Error: Tavily Search components could not be imported.")
        return {
            "raw_news": existing_news + [f"Automated monitoring active for {supplier['city']} region. Service offline."],
            "logs": ["Researcher: Import error encountered."],
            "search_count": 1
        }
    
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if tavily_api_key:
        try:
            search = TavilySearch(max_results=5)
            search_results = search.invoke(query)
            
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

    
    updated_news = existing_news + real_news

    return {
        "raw_news": updated_news,
        "logs": [f"Researcher: Processed web query (Attempt {current_attempt}). Fetched {len(real_news)} new items."],
        "search_count": 1 
    }