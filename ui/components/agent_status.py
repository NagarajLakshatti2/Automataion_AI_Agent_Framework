"""
Agent status component for Streamlit.
"""
import streamlit as st
from core.agents import AgentOrchestrator
from datetime import datetime


def render_agent_interface():
    """Render the agent interface."""
    # Initialize agent orchestrator
    if "agent_orchestrator" not in st.session_state:
        st.session_state.agent_orchestrator = AgentOrchestrator()

    # Initialize activity feed
    if "agent_activity" not in st.session_state:
        st.session_state.agent_activity = []

    orchestrator = st.session_state.agent_orchestrator

    # Display all agents
    st.subheader("Available Agents")

    agents = orchestrator.list_agents()

    # Display agents in a grid
    cols = st.columns(min(3, len(agents)))
    for i, agent in enumerate(agents):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="agent-card">
                <h3>🤖 {agent['name']}</h3>
                <p><strong>Type:</strong> {agent['type']}</p>
                <p><strong>Status:</strong> <span class="status-active">Active</span></p>
            </div>
            """, unsafe_allow_html=True)

    # Manual agent execution
    st.markdown("---")
    st.subheader("Execute Agent Task")

    col1, col2 = st.columns(2)

    with col1:
        agent_type = st.selectbox(
            "Select Agent",
            [agent['type'] for agent in agents],
            format_func=lambda x: next(a['name'] for a in agents if a['type'] == x)
        )

    with col2:
        task_description = st.text_input("Task Description")

    if st.button("Execute"):
        if task_description:
            with st.spinner("Executing task..."):
                try:
                    result = orchestrator.execute_task(agent_type, task_description, {})
                    st.success("Task completed!")
                    st.code(result, language="text")

                    # Add to activity feed
                    st.session_state.agent_activity.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "agent": agent_type,
                        "task": task_description,
                        "status": "completed"
                    })
                    # Keep only last 20 activities
                    st.session_state.agent_activity = st.session_state.agent_activity[:20]
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

                    # Add failed activity
                    st.session_state.agent_activity.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "agent": agent_type,
                        "task": task_description,
                        "status": "failed",
                        "error": str(e)
                    })
                    st.session_state.agent_activity = st.session_state.agent_activity[:20]
                    st.rerun()

    # Agent Activity Feed
    st.markdown("---")
    st.subheader("Agent Activity Feed")

    if st.session_state.agent_activity:
        for activity in st.session_state.agent_activity:
            status_icon = "✅" if activity["status"] == "completed" else "❌"
            status_class = "status-completed" if activity["status"] == "completed" else "status-failed"

            with st.expander(f"{status_icon} {activity['agent']} - {activity['timestamp']}"):
                st.markdown(f"""
                <div class="activity-item">
                    <p><strong>Agent:</strong> {activity['agent']}</p>
                    <p><strong>Task:</strong> {activity['task']}</p>
                    <p><strong>Status:</strong> <span class="{status_class}">{activity['status']}</span></p>
                </div>
                """, unsafe_allow_html=True)

                if activity["status"] == "failed" and "error" in activity:
                    st.error(f"Error: {activity['error']}")
    else:
        st.info("No agent activity yet. Execute a task to see activity here.")

    # Agent Health Check
    st.markdown("---")
    st.subheader("Agent Health Check")

    if st.button("Run Health Check"):
        with st.spinner("Checking agent health..."):
            try:
                health_status = orchestrator.get_agent_status()
                for agent_type, status in health_status.items():
                    if status["available"]:
                        st.success(f"✅ {agent_type}: Available")
                    else:
                        st.error(f"❌ {agent_type}: Unavailable")
            except Exception as e:
                st.error(f"Health check failed: {str(e)}")

    # Clear activity button
    if st.button("Clear Activity Feed"):
        st.session_state.agent_activity = []
        st.rerun()
