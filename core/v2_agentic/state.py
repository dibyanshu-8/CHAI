#Agent's shared memory
from typing import TypedDict,List,Annotated
import operator

class AgentState(TypedDict):
    raw_news:List[str]
    supplier_info:dict
    identified_risks:List[dict]
    final_alert:str
    logs:Annotated[List[str],operator.add]