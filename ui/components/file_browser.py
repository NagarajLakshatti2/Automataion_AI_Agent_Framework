"""
File browser component for Streamlit.
"""
import streamlit as st
from pathlib import Path
from config.settings import settings


def render_file_browser():
    """Render a file browser component."""
    project_root = Path(settings.AI_PROJECT_ROOT)

    st.subheader("File Browser")

    # Search input
    search = st.text_input("Search files...")

    # Get files
    files = []
    for file_path in project_root.rglob("*"):
        if file_path.is_file():
            if search and search.lower() not in file_path.name.lower():
                continue
            files.append(file_path)

    # Display files
    for file_path in files[:50]:  # Limit to 50 files
        with st.expander(f"📄 {file_path.name}"):
            st.write(f"**Path:** {file_path.relative_to(project_root)}")
            st.write(f"**Size:** {file_path.stat().st_size} bytes")

            if st.button(f"Read {file_path.name}", key=str(file_path)):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    st.code(content, language="text")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
