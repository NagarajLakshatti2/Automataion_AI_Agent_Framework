"""
Chat interface component for Streamlit.
"""
import streamlit as st
from typing import List, Dict, Any
from core.llm import get_llm_provider, Message
from config.prompts import Prompts


@st.cache_resource
def get_rag_retriever():
    """Cache the RAG retriever to avoid reloading embedding model."""
    from rag.retriever import ContextRetriever
    return ContextRetriever()


def render_chat_interface():
    """Render the chat interface."""
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize RAG enabled state
    if "rag_enabled" not in st.session_state:
        st.session_state.rag_enabled = False

    # RAG toggle
    rag_enabled = st.checkbox("Enable RAG (Context-Aware)", value=st.session_state.rag_enabled)
    st.session_state.rag_enabled = rag_enabled

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Display RAG context if available
            if "rag_context" in message and message["rag_context"]:
                with st.expander("📚 Retrieved Context"):
                    st.markdown(message["rag_context"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    llm = get_llm_provider()

                    # Build messages for LLM
                    messages = [
                        Message(role="system", content=Prompts.GENERAL)
                    ]

                    # Add RAG context if enabled
                    rag_context = ""
                    if rag_enabled:
                        try:
                            retriever = get_rag_retriever()
                            rag_context = retriever.retrieve_context(prompt, n_results=2)  # Reduced from 3 to 2

                            if rag_context and "No relevant code context found" not in rag_context:
                                # Add RAG context to system prompt
                                messages[0] = Message(
                                    role="system",
                                    content=Prompts.GENERAL + "\n\n" + Prompts.RAG_CONTEXT + "\n\n" + rag_context
                                )
                        except Exception as e:
                            st.warning(f"RAG retrieval failed: {str(e)}")

                    # Add conversation history (reduced from 10 to 5 for performance)
                    for msg in st.session_state.messages[-5:]:
                        messages.append(Message(role=msg["role"], content=msg["content"]))

                    # Generate response with streaming
                    response_placeholder = st.empty()
                    full_response = ""

                    try:
                        # Try streaming first
                        for chunk in llm.stream_chat(messages):
                            full_response += chunk
                            response_placeholder.markdown(full_response + "▌")
                        response_placeholder.markdown(full_response)
                    except Exception:
                        # Fallback to non-streaming if streaming fails
                        response = llm.chat(messages)
                        full_response = response.content
                        response_placeholder.markdown(full_response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response,
                        "rag_context": rag_context if rag_enabled else None
                    })

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
