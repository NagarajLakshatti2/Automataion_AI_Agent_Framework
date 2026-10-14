"""
Agents page for JeshlaAIAgent.
"""
import streamlit as st


def render_agents_page():
    """Render the agents page."""
    st.title("🤖 Agents")
    st.markdown("View and manage specialized agents.")

    # Agent interface
    from ui.components.agent_status import render_agent_interface
    render_agent_interface()
