import json
import re

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from typing import Literal

from collections import defaultdict
from agent.state import AgentState
from services.llm import get_llm
from agent.tools import get_account_info, get_recent_transactions, report_fraud

from model.xgb.predictions import predict_xgb

llm = get_llm().bind_tools([get_account_info,get_recent_transactions,report_fraud])
llm_no_tools = get_llm()


def risk_node(state: AgentState) -> dict:
    print("NODE: risk_node")

    txn = state["transaction"]

    xgb_score = predict_xgb(txn)
    score = float(xgb_score)

    if score > 0.9:
        level = "HIGH"
    elif score > 0.7:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "model_outputs": {
            "xgboost": {"score": score}
        },
        "fraud_score": score,
        "risk_level": level
    }

def risk_decision_edge(state: AgentState) -> str:
    print("EDGE: risk_decision_edge")

    level = state.get("risk_level")

    if level == "HIGH":
        return "investigate"
    elif level == "MEDIUM":
        return "review"
    else:
        return "safe"

def react_agent_node(state: AgentState) -> dict:
    print("NODE: react_agent_node")

    txn = state["transaction"]
    messages = state["messages"]
    steps = state.get("steps", 0)

    if steps > 6:
        print("Max steps reached")
        return {}

    # initialize only once
    if len(messages) == 0:
        messages = [
                SystemMessage(content=f"""
                    You are a fraud detection agent.

                    Available tools:
                    - get_account_info
                    - get_recent_transactions

                    Instructions:
                    - Analyze the transaction thoroughly
                    - Use tools if needed (max 5 calls)
                    - Then make a FINAL decision

                    RULES:
                    - NO markdown
                    - NO explanation outside JSON
                    --------------------------------------
                    """),
                HumanMessage(content=f"Analyze this transaction: {txn}")
            ]

    response = llm.invoke(messages)

    return {
        "messages": [response],
        "steps": steps + 1
    }

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    print("EDGE: should_continue")
    
    messages = state.get("messages", [])

    if not messages: 
        return "end"

    last = messages[-1]

    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"

    return "end"

def pattern_node(state: AgentState) -> AgentState:
    print("NODE: pattern_node")

    txn = state["transaction"]
    messages = state["messages"]

    txns = []

    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name == "get_recent_transactions":
            data = json.loads(msg.content)
            txns.extend(data)


    prompt = f"""
        Classify fraud pattern ONLY.

        Transaction: {txn}
        Related: {txns}

        Pattern definitions:

        - fan-in: many accounts send funds into one account
        - fan-out: one account sends funds to many accounts
        - gather-scatter: funds collected then redistributed
        - layering: multi-hop chain (A→B→C→D)
        - smurfing: many small transactions to avoid detection
        - cycle: circular money movement (A→B→C→A)
        - self-loop: account sends money to itself
        - burst: rapid high-frequency transactions
        - random: no clear pattern
        - stack: repeated transactions between same accounts

        Rules:
        - Choose EXACTLY one value from above or a compination of few values e.g. "Cycle + stack"
        - Do NOT create new names
        - Do NOT modify names
        - If unsure → return "unknown"

        Return JSON:
        {{
            "patternType": string
        }}
        """

    response = llm_no_tools.invoke(prompt)
    parsed = json.loads(clean_json_output(response.content))

    return {
        "pattern": parsed["patternType"],
        "related_transactions":txns
    }

def diagram_node(state: AgentState) -> dict:
    print("NODE: diagram_node")

    txn = state["transaction"]
    related = state.get("related_transactions", [])

    all_txns = [txn] + related

    edge_map = defaultdict(list)
    nodes = set()

    for t in all_txns:
        f = t["fromAccount"]
        to = t["toAccount"]

        nodes.add(f)
        nodes.add(to)

        edge_map[(f, to)].append(t)

    diagram = "graph LR\n"

    # nodes
    for n in nodes:
        diagram += f'{n}["{n}"]\n'

    # edges (aggregated)
    for (f, to), txns in edge_map.items():
        count = len(txns)
        total = sum(t["amountPaid"] for t in txns)

        label = f"{count} txns | {round(total,2)}"

        diagram += f'{f} -->|{label}| {to}\n'

    return {
        "diagram": diagram
    }

def final_decision_node(state: AgentState) -> dict:
    print("NODE: final_decision_node")

    txn = state["transaction"]
    pattern = state["pattern"]
    messages = state["messages"]
    risk_level = state["risk_level"]

    fraud_score = state.get("fraud_score", 0)

    prompt = f"""
        Generate fraud explanation

        Tools:
        report_fraud(txn)

        Transaction: {txn}
        Possible Pattern: {pattern}
        Fraud Score: {fraud_score}
        Risk Level: {risk_level}

        Return JSON:

        {{
            "reason": string,
            "isFraud": boolean
        }}

        Rules:
        - If fraud → explain why suspicious and call the report_fraud tool
        - If not → explain why safe
        - Be precise and factual
        - No markdown


        """

    response = llm_no_tools.invoke(messages + [HumanMessage(content=prompt)])
    

    try:
        parsed = json.loads(clean_json_output(response.content))
        reason = parsed.get("reason", "")
        is_fraud = parsed.get("isFraud", False)

    except Exception as e:
        print(e)
        reason = "Unable to generate explanation"
        is_fraud = False

    return {
        "messages": messages,
        "isFraud": is_fraud,
        "reason": reason
    }

def final_reporting_node(state: AgentState) -> dict:
    print("NODE: final_reporting_node")

    txn = state["transaction"]
    analysis = state.get("analysis", {})
    messages = state.get("messages", [])
    reason = state.get("reason", [])


    prompt = f"""
        You are a fraud reporting agent.

        If the transaction is fraud, you MUST call the tool `report_fraud`.

        Transaction:
        {txn}

        Analysis:
        {analysis}

        Reason:
        {reason}

        Rules:
        - If isFraud = true → call report_fraud
        - Choose blacklist_level:
            - BLACK → high risk
            - GREY → medium risk

        DO NOT return JSON.
        ONLY call the tool if fraud.
    """

    response = llm.invoke(messages + [HumanMessage(content=prompt)])

    return {
        "messages": [response]
    }



def clean_json_output(text: str) -> str:
    text = text.strip()

    # remove ```json ... ```
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)

    return text.strip()