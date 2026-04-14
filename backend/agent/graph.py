from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from agent.state import AgentState
from agent.nodes import diagram_node, final_decision_node, final_reporting_node, pattern_node, react_agent_node, risk_decision_edge, risk_node, should_continue
from agent.tools import get_account_info, get_recent_transactions, report_fraud

tools = [get_account_info, get_recent_transactions, report_fraud]

def build_graph():
    builder = StateGraph(AgentState)

    tool_node = ToolNode([
        get_account_info,
        get_recent_transactions
    ])

    report_tool_node = ToolNode([report_fraud])

    builder.add_node("risk", risk_node)
    builder.add_node("agent", react_agent_node)
    builder.add_node("tools", tool_node)
    builder.add_node("pattern", pattern_node)
    builder.add_node("diagram", diagram_node)
    builder.add_node("final", final_decision_node)
    builder.add_node("report_fraud", final_reporting_node)
    builder.add_node("report_tool", report_tool_node)

    builder.set_entry_point("risk")

    # Risk routing
    builder.add_conditional_edges(
        "risk",
        risk_decision_edge,
        {
            "safe": END,
            "review": "agent",
            "investigate": "agent"
        }
    )

    # ReAct loop
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": "pattern"
        }
    )

    builder.add_edge("tools", "agent")

    # Analysis pipeline
    builder.add_edge("pattern", "diagram")
    builder.add_edge("diagram", "final")

    # 🔥 NEW FLOW
    builder.add_edge("final", "report_fraud")

    builder.add_conditional_edges(
        "report_fraud",
        should_continue,
        {
            "tools": "report_tool",
            "end": END
        }
    )

    builder.add_edge("report_tool", END)

    return builder.compile()