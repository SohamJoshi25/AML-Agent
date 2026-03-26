from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from agent.state import AgentState
from agent.nodes import agent_node, should_continue
from agent.tools import get_account_info, get_recent_transactions, report_fraud

tools = [get_account_info, get_recent_transactions, report_fraud]

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    graph.add_edge("tools", "agent")

    return graph.compile()