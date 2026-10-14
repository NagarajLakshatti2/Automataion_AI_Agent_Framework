"""
Terminal component for displaying execution logs.
"""
import streamlit as st
from typing import List, Dict, Any


def render_terminal(logs: List[str]):
    """
    Render a terminal-like component for logs.

    Args:
        logs: List of log messages
    """
    st.subheader("Terminal Output")

    if not logs:
        st.info("No logs to display.")
        return

    for log in logs:
        st.text(log)
