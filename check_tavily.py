from langchain_tavily import TavilySearch
import os

# We can't create a real instance without API key, but let's at least import the wrapper class
# Let's look at what TavilySearch would use
try:
    # Try to inspect the source
    import inspect
    from langchain_tavily.utils import TavilyAPIWrapper
    
    print("TavilyAPIWrapper methods:")
    methods = [m for m in dir(TavilyAPIWrapper) if not m.startswith('_')]
    for m in methods:
        print(f"  - {m}")
        
    # Check for raw_results specifically
    if hasattr(TavilyAPIWrapper, 'raw_results'):
        sig = inspect.signature(TavilyAPIWrapper.raw_results)
        print(f"\nraw_results signature: {sig}")
except ImportError as e:
    print(f"Could not import TavilyAPIWrapper: {e}")
    
    # Try alternative
    try:
        from langchain_community.tools.tavily_search.tool import TavilySearchAPIWrapper
        print("Found TavilySearchAPIWrapper in langchain_community")
        methods = [m for m in dir(TavilySearchAPIWrapper) if not m.startswith('_') and 'result' in m.lower()]
        print(f"Methods with 'result': {methods}")
    except ImportError as e2:
        print(f"Could not import from langchain_community either: {e2}")
