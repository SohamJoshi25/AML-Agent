from typing import List, TypedDict, Annotated, Sequence

from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    transaction: Annotated[dict,"The transaction current user is refering to and wants to analyze"]
    messages: Annotated[Sequence[BaseMessage], add_messages]