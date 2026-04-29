import time

import streamlit as st

from src.core.config import settings


def check_rate_limit():
    """Returns True if user is within the RPM limit defined in settings."""
    if "request_timestamps" not in st.session_state:
        st.session_state.request_timestamps = []
        
    now = time.time()
    # Remove timestamps older than 60 seconds
    st.session_state.request_timestamps = [
        t for t in st.session_state.request_timestamps if now - t < 60
    ]
    
    if len(st.session_state.request_timestamps) >= settings.rate_limit_rpm:
        return False
    return True


def record_request():
    """Logs a new request timestamp."""
    st.session_state.request_timestamps.append(time.time())
