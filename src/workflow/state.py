from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    """The graph state definition."""
    # The messages key handles appending new messages to the list
    messages: Annotated[list, add_messages]
    user_id: str
