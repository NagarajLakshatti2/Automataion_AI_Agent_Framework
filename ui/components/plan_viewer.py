"""
Plan viewer component for Streamlit.
"""
import streamlit as st
from core.planner import TaskPlanner, PlanExecutor, PlanTracker
from core.agents import AgentOrchestrator


def render_plan_interface():
    """Render the plan interface."""
    # Initialize components
    if "task_planner" not in st.session_state:
        st.session_state.task_planner = TaskPlanner()
    if "plan_tracker" not in st.session_state:
        st.session_state.plan_tracker = PlanTracker()
    if "agent_orchestrator" not in st.session_state:
        st.session_state.agent_orchestrator = AgentOrchestrator()

    # Input for goal
    st.subheader("Create a Plan")
    goal = st.text_area("What would you like to accomplish?", height=100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Plan"):
            if goal:
                with st.spinner("Generating plan..."):
                    try:
                        plan = st.session_state.task_planner.create_plan(goal)
                        st.session_state.current_plan = plan
                        st.success("Plan generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating plan: {str(e)}")

    with col2:
        if st.button("Clear Current Plan"):
            if "current_plan" in st.session_state:
                del st.session_state.current_plan
                st.rerun()

    # Display current plan
    if "current_plan" in st.session_state:
        st.markdown("---")
        st.subheader("Current Plan")

        plan = st.session_state.current_plan

        # Plan summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(plan.tasks))
        with col2:
            completed = sum(1 for t in plan.tasks if t.status.value == "completed")
            st.metric("Completed", completed)
        with col3:
            st.metric("Status", plan.status.value)

        st.write(f"**Goal:** {plan.goal}")

        # Progress bar
        if len(plan.tasks) > 0:
            progress = completed / len(plan.tasks) * 100
            st.progress(progress / 100)

        # Display tasks with editing
        st.markdown("### Tasks")
        for i, task in enumerate(plan.tasks, 1):
            complexity_class = f"complexity-{task.complexity.value}"

            with st.expander(f"Task {i}: {task.description} ({task.status.value})"):
                # Task editing
                col1, col2 = st.columns(2)
                with col1:
                    new_description = st.text_input(
                        "Description",
                        value=task.description,
                        key=f"task_{i}_desc"
                    )
                with col2:
                    new_agent = st.selectbox(
                        "Agent",
                        ["auto", "code_generator", "file_agent", "git_agent", "test_agent",
                         "debug_agent", "refactor_agent", "code_converter", "code_reviewer"],
                        index=["auto", "code_generator", "file_agent", "git_agent", "test_agent",
                                "debug_agent", "refactor_agent", "code_converter", "code_reviewer"].index(
                            task.agent_type if task.agent_type else "auto"
                        ),
                        key=f"task_{i}_agent"
                    )

                if st.button(f"Update Task {i}", key=f"update_task_{i}"):
                    task.description = new_description
                    task.agent_type = new_agent
                    st.success(f"Task {i} updated!")
                    st.rerun()

                st.markdown(f"""
                <div class="task-item {complexity_class}">
                    <p><strong>Complexity:</strong> {task.complexity.value}</p>
                    <p><strong>Agent:</strong> {task.agent_type or 'auto'}</p>
                </div>
                """, unsafe_allow_html=True)

                if task.dependencies:
                    st.write(f"**Dependencies:** {task.dependencies}")
                if task.result:
                    st.write(f"**Result:** {task.result}")
                if task.error:
                    st.error(f"**Error:** {task.error}")

        # Plan actions
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Execute Plan"):
                executor = PlanExecutor(st.session_state.agent_orchestrator)

                def on_progress(progress, task):
                    st.progress(progress / 100, text=f"Executing: {task.description}")

                with st.spinner("Executing plan..."):
                    try:
                        executed_plan = executor.execute_plan(
                            plan,
                            on_progress=on_progress
                        )
                        st.session_state.current_plan = executed_plan
                        st.success("Plan execution completed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error executing plan: {str(e)}")

        with col2:
            if st.button("Save Plan"):
                try:
                    st.session_state.plan_tracker.save_plan(plan)
                    st.success("Plan saved!")
                except Exception as e:
                    st.error(f"Error saving plan: {str(e)}")

        with col3:
            if st.button("Export Plan"):
                import json
                plan_json = plan.to_dict()
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(plan_json, indent=2),
                    file_name=f"plan_{plan.id}.json",
                    mime="application/json"
                )

    # Plan history
    st.markdown("---")
    st.subheader("Plan History")

    plans = st.session_state.plan_tracker.list_plans(limit=10)

    if plans:
        for plan_summary in plans:
            with st.expander(f"{plan_summary['goal'][:50]}... ({plan_summary['status']})"):
                st.write(f"**ID:** {plan_summary['id']}")
                st.write(f"**Created:** {plan_summary['created_at']}")
                st.write(f"**Tasks:** {plan_summary['task_count']}")

                # Load plan button
                if st.button(f"Load Plan {plan_summary['id'][:8]}", key=f"load_{plan_summary['id']}"):
                    loaded_plan = st.session_state.plan_tracker.load_plan(plan_summary['id'])
                    if loaded_plan:
                        st.session_state.current_plan = loaded_plan
                        st.success("Plan loaded!")
                        st.rerun()
    else:
        st.info("No plans in history yet.")
