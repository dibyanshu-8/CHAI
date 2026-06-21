# langgraph implementation
from langgraph.graph import StateGraph, END 
from core.v2_agentic.state import AgentState
from core.v2_agentic.agents.researcher import researcher_node
from core.v2_agentic.agents.analyst import analyst_node
from core.v2_agentic.agents.alerter import alerter_node

def router_logic(state: AgentState) -> str:
    """
    The "Brain" of the autonomous routing. 
    Decides whether to loop back for more research or proceed to reporting.
    """
    search_count = state.get("search_count", 0)
    is_sufficient = state.get("is_data_sufficient", True)

    if search_count >= 2:
        print("Router: Max searches (2) reached. Forcing to Alert generation.")
        return "alert"
    
    # Autonomous LLM Decision
    if is_sufficient:
        print("Router: Analyst confirmed data is sufficient. Proceeding to Alert.")
        return "alert"
    else:
        print("Router: Analyst requested more data. Looping back to Researcher.")
        return "research"

def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("research", researcher_node)
    workflow.add_node("analyze", analyst_node)
    workflow.add_node("alert", alerter_node)

    # Set Entry Point
    workflow.set_entry_point("research")

    # Autonomous Control Flow
    workflow.add_edge("research", "analyze")
    
    # Conditional Routing 
    workflow.add_conditional_edges(
        "analyze",            
        router_logic,         
        {
            "research": "research",  
            "alert": "alert"         
        }
    )

   
    workflow.add_edge("alert", END)

    return workflow.compile()