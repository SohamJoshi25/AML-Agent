from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import Literal

from agent.state import AgentState
from services.llm import get_llm
from agent.tools import get_account_info, get_recent_transactions, report_fraud, get_xgboost_prediction

llm = get_llm().bind_tools([
    get_account_info,
    get_recent_transactions,
    report_fraud,
    get_xgboost_prediction
])


def agent_node(state: AgentState) -> AgentState:
    print("NODE: agent_node")

    transaction = state.get("transaction", None)
    messages = list(state.get("messages", []))

    if not messages:
        messages = [
            SystemMessage(content="""
                You are a fraud detection agent.

                Available tools:
                - get_account_info
                - get_recent_transactions
                - report_fraud
                - get_xgboost_prediction IMP

                Instructions:
                - Analyze the transaction
                - Call tools if needed,: get_xgboost_prediction, get_account_info
                - If fraud, call report_fraud

                STRICT RULES:

                1. FIRST call get_xgboost_prediction
                2. THEN optionally call get_recent_transactions (max 3 time)
                3. THEN MUST make a decision
                4. NEVER call the same tool more than once per account
                5. MAX 7 tool calls total

                Do not ask for more info.
                """),
            HumanMessage(content=f"Analyze this transaction: {transaction}")
        ]
    
    response = llm.invoke(messages)
    print("Content:", response.content)
    print("Tool calls:", response.tool_calls)
    print()
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