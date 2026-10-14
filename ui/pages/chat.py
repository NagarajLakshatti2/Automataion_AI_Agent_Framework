"""
Chat page for JeshlaAIAgent.
"""
import streamlit as st


def render_chat_page():
    """Render the chat page."""
    st.title("💬 Chat")
    st.markdown("Interact with JeshlaAIAgent using natural language.")

    # Chat interface
    from ui.components.chat_interface import render_chat_interface
    render_chat_interface()
