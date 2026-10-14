"""
Code editor component for Streamlit.
"""
import streamlit as st


def render_code_editor(code: str, language: str = "python", height: int = 400):
    """
    Render a code editor component.

    Args:
        code: Code to display/edit
        language: Programming language for syntax highlighting
        height: Height of the editor in pixels
    """
    st.code(code, language=language, height=height)
