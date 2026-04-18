from typing import Any, Dict, List, Optional, TypedDict, Annotated, Sequence

from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    transaction: Annotated[dict,"The transaction current user is refering to and wants to analyze"]
    messages: Annotated[Sequence[BaseMessage], add_messages]

    related_transactions: Optional[List[dict]]

    fraud_score: Optional[float]
    risk_level: Optional[str]
    is_fraud: Optional[bool]

    steps: Optional[int]
    pattern: Optional[str]
    diagram: Optional[str]
    reason: Optional[str]
    analysis: Optional[dict]