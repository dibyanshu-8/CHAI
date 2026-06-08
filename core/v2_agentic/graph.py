#langgraph implementation
from langgraph.graph import StateGraph, END 
from core.v2_agentic.state import AgentState
from core.v2_agentic.agents.researcher import researcher_node
from core.v2_agentic.agents.analyst import analyst_node
from core.v2_agentic.agents.alerter import alerter_node

def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("research", researcher_node)
    workflow.add_node("analyze", analyst_node)
    workflow.add_node("alert", alerter_node)

    # Set Entry Point
    workflow.set_entry_point("research")

    # Define Edges (The Path)
    workflow.add_edge("research", "analyze")
    workflow.add_edge("analyze", "alert")
    workflow.add_edge("alert", END)

    return workflow.compile()