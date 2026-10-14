"""
Settings panel component for Streamlit.
"""
import streamlit as st
from config.settings import settings


def render_settings_panel():
    """Render the settings panel."""
    st.subheader("Settings")

    # LLM Provider
    st.write("**LLM Provider**")
    current_provider = settings.LLM_PROVIDER
    st.info(f"Current: {current_provider}")

    st.write("**Model Configuration**")
    if current_provider == "ollama":
        st.text_input("Ollama Model", value=settings.OLLAMA_MODEL, disabled=True)
        st.text_input("Ollama URL", value=settings.OLLAMA_URL, disabled=True)
    elif current_provider == "openrouter":
        st.text_input("OpenRouter Model", value=settings.OPENROUTER_MODEL, disabled=True)
    elif current_provider == "google":
        st.text_input("Google Model", value=settings.GOOGLE_MODEL, disabled=True)

    st.markdown("---")

    # Project Settings
    st.write("**Project Settings**")
    st.text_input("Project Root", value=settings.AI_PROJECT_ROOT, disabled=True)

    st.markdown("---")

    # RAG Settings
    st.write("**RAG Settings**")
    st.text_input("Embedding Model", value=settings.EMBEDDING_MODEL, disabled=True)
    st.number_input("Chunk Size", value=settings.CHUNK_SIZE, disabled=True)
    st.number_input("Chunk Overlap", value=settings.CHUNK_OVERLAP, disabled=True)

    st.markdown("---")

    # App Info
    st.write("**Application Info**")
    st.text_input("App Name", value=settings.APP_NAME, disabled=True)
    st.text_input("Version", value=settings.APP_VERSION, disabled=True)
    st.checkbox("Debug Mode", value=settings.DEBUG, disabled=True)

    st.info("To change settings, edit the .env file and restart the application.")
