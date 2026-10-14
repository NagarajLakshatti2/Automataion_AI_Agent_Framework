"""
Main Streamlit application for JeshlaAIAgent.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from pathlib import Path


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="JeshlaAIAgent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    # Load custom CSS
    css_path = Path(__file__).parent / "styles" / "custom.css"
    with open(css_path, "r") as f:
        custom_css = f.read()
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

    # Apply theme to the app
    st.markdown(f"""
    <style>
    .stApp {{
        data-theme: {st.session_state.theme};
    }}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("🤖 JeshlaAIAgent")
        st.markdown("---")

        # Navigation
        page = st.radio(
            "Navigate",
            ["Chat", "Plan", "Agents"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Theme toggle
        st.subheader("Appearance")
        theme = st.selectbox(
            "Theme",
            ["dark", "light"],
            index=0 if st.session_state.theme == "dark" else 1,
            key="theme_selector"
        )
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()

        st.markdown("---")

        # Settings
        st.subheader("Settings")

        # LLM Provider
        from config.settings import settings
        current_provider = settings.LLM_PROVIDER

        llm_provider = st.selectbox(
            "LLM Provider",
            ["ollama", "openrouter", "google"],
            index=["ollama", "openrouter", "google"].index(current_provider) if current_provider in ["ollama", "openrouter", "google"] else 0
        )

        # Model selection based on provider
        if llm_provider == "ollama":
            st.text_input("Ollama Model", value=settings.OLLAMA_MODEL, disabled=True)
        elif llm_provider == "openrouter":
            st.text_input("OpenRouter Model", value=settings.OPENROUTER_MODEL, disabled=True)
        elif llm_provider == "google":
            st.text_input("Google Model", value=settings.GOOGLE_MODEL, disabled=True)

        st.markdown("---")

        # Project Root
        st.text_input("Project Root", value=settings.AI_PROJECT_ROOT, disabled=True)

        st.markdown("---")

        # RAG Settings
        st.subheader("RAG Settings")
        st.write("RAG (Retrieval-Augmented Generation) enables context-aware responses by indexing your codebase.")
        st.caption("Index your codebase in the Chat section to enable RAG features.")

        st.markdown("---")

        # Info
        st.caption(f"Version: {settings.APP_VERSION}")
        st.caption("Built with Streamlit & LangChain")

    # Main content based on page selection
    if page == "Chat":
        from ui.pages.chat import render_chat_page
        render_chat_page()
    elif page == "Plan":
        from ui.pages.plan import render_plan_page
        render_plan_page()
    elif page == "Agents":
        from ui.pages.agents import render_agents_page
        render_agents_page()


if __name__ == "__main__":
    main()
