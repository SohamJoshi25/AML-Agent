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
                - get_xgboost_prediction (MANDATORY FIRST STEP)

                Instructions:
                - Analyze the transaction thoroughly
                - FIRST call get_xgboost_prediction
                - Optionally call get_account_info or get_recent_transactions (max 3 times)
                - Then make a FINAL decision
                - if multiple accounts send funds into one account, classify as "fan-in" or "gather".
                - If that account then sends funds outward, classify as "gather-scatter".
                - Do NOT classify this as layering unless there are multi-hop chains (A→B→C→D).

                STRICT RULES:
                1. FIRST call get_xgboost_prediction
                2. THEN optionally call get_recent_transactions (max 3 times)
                3. THEN MUST make a decision
                4. NEVER call the same tool more than once per account
                5. MAX 7 tool calls total
                6. DO NOT ask for more info

                FINAL OUTPUT FORMAT:

                If NOT fraud:
                - Explain why it's safe

                If FRAUD:
                - Explain why it's fraud
                - Identify pattern type (e.g., smurfing, layering, rapid movement, fan-in, fan-out)
                - Generate a Mermaid diagram showing flow of money between entities

                Mermaid format example:

                ```
                graph LR
                A[Account A] -->|Transfer| B[Account B]
                B -->|Transfer| C[Account C]```

                Follow proper Mermaid diagram format. 

                Diagram must include:
                - All unique accounts involved
                - Direction of flow
                - Self Loops if present (self Transfer)

                Always consider ALL accounts returned from get_recent_transactions.
                Do not focus only on the transaction pair.
                
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