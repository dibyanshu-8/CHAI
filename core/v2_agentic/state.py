# Agent's shared memory
from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    raw_news: List[str]
    supplier_info: dict
    identified_risks: List[dict]
    final_alert: str
    logs: Annotated[List[str], operator.add]
    
    # Autonomous routing variables
    search_count: Annotated[int, operator.add] 
    
    
    is_data_sufficient: bool