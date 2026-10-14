"""
Plan page for JeshlaAIAgent.
"""
import streamlit as st


def render_plan_page():
    """Render the plan page."""
    st.title("📋 Plan")
    st.markdown("Create and execute plans for complex tasks.")

    # Plan interface
    from ui.components.plan_viewer import render_plan_interface
    render_plan_interface()
