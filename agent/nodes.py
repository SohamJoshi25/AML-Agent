from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import Literal

from agent.state import AgentState
from services.llm import get_llm
from agent.tools import get_account_info, get_recent_transactions, report_fraud

llm = get_llm().bind_tools([
    get_account_info,
    get_recent_transactions,
    report_fraud
])


def agent_node(state: AgentState) -> AgentState:
    print("NODE: agent_node")

    transaction = state.get("transaction", None)
    messages = list(state.get("messages", []))

    if not messages:
        messages = [
            SystemMessage(content="""
                You are a fraud detection agent.

                Rules:
                - Call only ONE tool at a time
                - Never invent values
                - Use only given transaction or tool data

                Process:
                1. Extract account_id and amount
                2. Call get_account_info(account_id)
                3. Analyze the transaction using tool call.


                Action:
                - If fraud is suspected → call report_fraud(account_id, amount, reason)
                - Else → return explanation (no tool call)

                Do not ask for more info.
                """),
            HumanMessage(content=f"Analyze this transaction: {transaction}")
        ]
    
    response = llm.invoke(messages)

    return {
        "messages": messages + [response]
    }



def should_continue(state: AgentState) -> Literal["tools", "end"]:
    print("EDGE: should_continue")
    
    messages = state.get("messages", [])

    last = messages[-1]

    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"

    return "end"