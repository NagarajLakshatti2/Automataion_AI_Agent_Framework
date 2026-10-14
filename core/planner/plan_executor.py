"""
Plan Executor for executing plans step by step.
"""
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from .task_planner import Plan, Task, TaskStatus


class PlanExecutor:
    """Executes plans by coordinating agents."""

    def __init__(self, agent_orchestrator=None):
        """
        Initialize the plan executor.

        Args:
            agent_orchestrator: Optional agent orchestrator instance
        """
        self.agent_orchestrator = agent_orchestrator
        self.current_plan: Optional[Plan] = None
        self.execution_callbacks: Dict[str, Callable] = {}

    def set_agent_orchestrator(self, agent_orchestrator):
        """
        Set the agent orchestrator.

        Args:
            agent_orchestrator: Agent orchestrator instance
        """
        self.agent_orchestrator = agent_orchestrator

    def execute_plan(
        self,
        plan: Plan,
        on_task_start: Optional[Callable] = None,
        on_task_complete: Optional[Callable] = None,
        on_task_fail: Optional[Callable] = None,
        on_progress: Optional[Callable] = None
    ) -> Plan:
        """
        Execute a plan by running its tasks in dependency order.

        Args:
            plan: The plan to execute
            on_task_start: Callback when a task starts
            on_task_complete: Callback when a task completes
            on_task_fail: Callback when a task fails
            on_progress: Callback with progress updates

        Returns:
            The executed plan with updated task statuses
        """
        self.current_plan = plan
        plan.status = TaskStatus.IN_PROGRESS

        # Store callbacks
        self.execution_callbacks = {
            "on_task_start": on_task_start,
            "on_task_complete": on_task_complete,
            "on_task_fail": on_task_fail,
            "on_progress": on_progress,
        }

        try:
            # Execute tasks in dependency order
            executed_tasks = set()
            total_tasks = len(plan.tasks)

            while len(executed_tasks) < total_tasks:
                # Find tasks that can be executed (dependencies satisfied)
                ready_tasks = self._find_ready_tasks(plan.tasks, executed_tasks)

                if not ready_tasks:
                    # Check if all remaining tasks have unmet dependencies
                    remaining = [t for t in plan.tasks if t.id not in executed_tasks]
                    if all(t.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED] for t in remaining):
                        break
                    else:
                        raise Exception("Circular dependency detected or unable to resolve dependencies")

                # Execute ready tasks
                for task in ready_tasks:
                    self._execute_task(task)
                    executed_tasks.add(task.id)

                    # Report progress
                    if on_progress:
                        progress = len(executed_tasks) / total_tasks * 100
                        on_progress(progress, task)

            # Check if all tasks completed successfully
            if all(t.status == TaskStatus.COMPLETED for t in plan.tasks):
                plan.status = TaskStatus.COMPLETED
            else:
                plan.status = TaskStatus.FAILED

        except Exception as e:
            plan.status = TaskStatus.FAILED
            raise

        finally:
            plan.updated_at = datetime.now()

        return plan

    def _find_ready_tasks(self, tasks: list, executed: set) -> list:
        """
        Find tasks that are ready to execute (dependencies satisfied).

        Args:
            tasks: List of all tasks
            executed: Set of executed task IDs

        Returns:
            List of ready tasks
        """
        ready = []
        for task in tasks:
            if task.id in executed:
                continue
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED]:
                continue

            # Check if all dependencies are executed
            deps_satisfied = all(dep_id in executed for dep_id in task.dependencies)
            if deps_satisfied:
                ready.append(task)

        return ready

    def _execute_task(self, task: Task):
        """
        Execute a single task using the appropriate agent.

        Args:
            task: The task to execute
        """
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()

        # Call task start callback
        if self.execution_callbacks.get("on_task_start"):
            self.execution_callbacks["on_task_start"](task)

        try:
            # Determine which agent to use
            agent_type = task.agent_type or self._infer_agent_type(task.description)

            # Execute the task using the agent
            if self.agent_orchestrator:
                result = self.agent_orchestrator.execute_task(
                    agent_type=agent_type,
                    task_description=task.description,
                    context=self._get_task_context(task)
                )
            else:
                # Fallback if no orchestrator is set
                result = f"Task executed (agent orchestrator not configured): {task.description}"

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()

            # Call task complete callback
            if self.execution_callbacks.get("on_task_complete"):
                self.execution_callbacks["on_task_complete"](task)

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()

            # Call task fail callback
            if self.execution_callbacks.get("on_task_fail"):
                self.execution_callbacks["on_task_fail"](task)

            raise

    def _infer_agent_type(self, description: str) -> str:
        """
        Infer the appropriate agent type from the task description.

        Args:
            description: Task description

        Returns:
            Agent type string
        """
        description_lower = description.lower()

        # Keywords for different agent types
        agent_keywords = {
            "code_generator": ["generate", "create", "write", "implement", "code"],
            "code_converter": ["convert", "translate", "migrate", "port"],
            "code_reviewer": ["review", "analyze", "check", "audit"],
            "file_agent": ["file", "read", "write", "save", "open", "edit"],
            "git_agent": ["git", "commit", "push", "pull", "branch", "merge"],
            "test_agent": ["test", "testing", "unit test", "coverage"],
            "debug_agent": ["debug", "fix", "error", "bug", "issue"],
            "refactor_agent": ["refactor", "improve", "optimize", "clean"],
        }

        # Find the best match
        for agent_type, keywords in agent_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return agent_type

        # Default to code_generator
        return "code_generator"

    def _get_task_context(self, task: Task) -> Dict[str, Any]:
        """
        Get context for executing a task.

        Args:
            task: The task being executed

        Returns:
            Context dictionary
        """
        context = {
            "task_id": task.id,
            "task_description": task.description,
            "dependencies": task.dependencies,
            "plan_goal": self.current_plan.goal if self.current_plan else None,
        }

        return context

    def pause_execution(self):
        """Pause the current plan execution."""
        # Implementation for pausing execution
        pass

    def resume_execution(self):
        """Resume a paused plan execution."""
        # Implementation for resuming execution
        pass

    def cancel_execution(self):
        """Cancel the current plan execution."""
        if self.current_plan:
            self.current_plan.status = TaskStatus.FAILED
            self.current_plan.updated_at = datetime.now()
