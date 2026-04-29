import os
import sys
import threading
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src.core.config import settings
from src.services.reflector import extract_and_store_facts
from src.ui.components import render_sidebar, save_thread_metadata
from src.utils.limiter import check_rate_limit, record_request
from src.workflow.builder import build_chatbot_graph


# Page Config
st.set_page_config(page_title="Personalized AI Assistant", page_icon="🧠", layout="wide")

# Main Header
st.title("🧠 Personalized AI Assistant")
st.markdown("Persistent long-term memory")

# --- Initialize Session State ---
if "user_id" not in st.session_state:
    st.session_state.user_id = settings.default_user_id
if "current_thread_id" not in st.session_state:
    st.session_state.current_thread_id = str(uuid.uuid4())


# --- Build Graph ---
@st.cache_resource
def get_graph():
    """Returns the compiled LangGraph workflow."""
    return build_chatbot_graph()


# Module-level Constant for the Graph
CHATBOT_GRAPH = get_graph()

# --- Sidebar ---
render_sidebar(CHATBOT_GRAPH)

# --- Chat Configuration ---
config = {
    "configurable": {
        "thread_id": st.session_state.current_thread_id,
        "user_id": st.session_state.user_id
    }
}


def run_reflection(history, user_id):
    """Background task to extract and store facts."""
    extract_and_store_facts(history, user_id, CHATBOT_GRAPH.store)


# --- Display Messages ---
try:
    state = CHATBOT_GRAPH.get_state(config)
    messages = state.values.get("messages", [])
except Exception as e:
    st.error(f"Error loading chat history: {e}")
    messages = []

for msg in messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        clean_content = msg.content.replace(settings.memory_tag, "").strip()
        if clean_content:
            with st.chat_message("assistant"):
                st.markdown(clean_content)

# --- Chat Input ---
if prompt := st.chat_input("What's on your mind?"):
    # 1. Rate Limit Check
    if not check_rate_limit():
        st.error(f"⚠️ Rate limit reached ({settings.rate_limit_rpm} RPM).")
        st.stop()
    
    # 2. Log Request
    record_request()
    
    # 3. Handle First Message (Thread Indexing)
    if not messages:
        save_thread_metadata(
            st.session_state.user_id, 
            st.session_state.current_thread_id, 
            CHATBOT_GRAPH, 
            prompt
        )
    
    # 4. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Invoke Graph
    with st.chat_message("assistant"):
        with st.spinner("Searching memory & thinking..."):
            input_data = {
                "messages": [HumanMessage(content=prompt)], 
                "user_id": st.session_state.user_id
            }
            response = CHATBOT_GRAPH.invoke(input_data, config=config)
            
            # Update thread metadata (timestamp)
            save_thread_metadata(
                st.session_state.user_id, 
                st.session_state.current_thread_id, 
                CHATBOT_GRAPH, 
                prompt
            )

            # Get response
            ai_msg = response["messages"][-1]
            content = ai_msg.content
            
            display_content = content.replace(settings.memory_tag, "").strip()
            st.markdown(display_content)
            
            # 6. Trigger Background Reflection if tagged
            if settings.memory_tag in content:
                print(f"DEBUG: Memory tag '{settings.memory_tag}' found! Triggering reflection...")
                full_history = response["messages"]
                thread = threading.Thread(
                    target=run_reflection, 
                    args=(full_history, st.session_state.user_id)
                )
                thread.start()
            else:
                print("DEBUG: No memory tag found in response.")
