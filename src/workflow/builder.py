from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

from src.workflow.state import State
from src.workflow.nodes import call_chatbot
from src.services.database import get_connection_pool
from src.services.embeddings import get_embeddings_provider
from src.core.config import settings


def build_chatbot_graph():
    """Constructs and compiles the LangGraph workflow."""
    pool = get_connection_pool()
    checkpointer = PostgresSaver(pool)
    
    store = PostgresStore(
        pool,
        index={
            "embed": get_embeddings_provider(),
            "dims": settings.embedding_dimensions,
            "fields": ["fact"]
        }
    )
    
    checkpointer.setup()
    store.setup()
    
    workflow = StateGraph(State)
    workflow.add_node("chatbot", call_chatbot)
    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)
    
    return workflow.compile(checkpointer=checkpointer, store=store)
