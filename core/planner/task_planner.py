"""
Task Planner for breaking down complex tasks into manageable steps.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from core.llm import get_llm_provider, Message


class TaskStatus(Enum):
    """Status of a task in the plan."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskComplexity(Enum):
    """Complexity level of a task."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """Represents a single task in a plan."""
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    complexity: TaskComplexity = TaskComplexity.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    estimated_time: Optional[int] = None  # in minutes
    agent_type: Optional[str] = None  # Which agent should handle this
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "complexity": self.complexity.value,
            "dependencies": self.dependencies,
            "estimated_time": self.estimated_time,
            "agent_type": self.agent_type,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class Plan:
    """Represents a complete plan with multiple tasks."""
    id: str
    goal: str
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.PENDING

    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary."""
        return {
            "id": self.id,
            "goal": self.goal,
            "tasks": [task.to_dict() for task in self.tasks],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
        }


class TaskPlanner:
    """Planner for breaking down complex tasks."""

    def __init__(self):
        """Initialize the task planner."""
        self.llm = get_llm_provider()

    def create_plan(self, goal: str, context: Optional[str] = None) -> Plan:
        """
        Create a plan from a goal.

        Args:
            goal: The main goal to achieve
            context: Optional context about the project/codebase

        Returns:
            A Plan object with tasks
        """
        import uuid
        plan_id = str(uuid.uuid4())

        # Build the planning prompt
        system_prompt = self._get_planning_prompt()
        user_prompt = self._build_planning_prompt(goal, context)

        # Get plan from LLM
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3  # Lower temperature for more structured output
        )

        # Parse the LLM response into tasks
        tasks = self._parse_plan_response(response.content)

        return Plan(
            id=plan_id,
            goal=goal,
            tasks=tasks
        )

    def _get_planning_prompt(self) -> str:
        """Get the system prompt for planning."""
        from config.prompts import Prompts
        return Prompts.get_prompt("task_planner")

    def _build_planning_prompt(self, goal: str, context: Optional[str]) -> str:
        """Build the user prompt for planning."""
        prompt = f"""Goal: {goal}

Please break this down into a series of specific, actionable tasks.

For each task, provide:
1. A clear description of what needs to be done
2. Dependencies (which tasks must be completed first)
3. Complexity level (low, medium, high, critical)
4. Estimated time in minutes
5. Which agent type should handle it (code_generator, file_agent, git_agent, test_agent, etc.)

Format your response as a numbered list with the following structure for each task:
Task X: [description]
Dependencies: [task numbers or "none"]
Complexity: [low/medium/high/critical]
Estimated Time: [minutes]
Agent: [agent type]
"""

        if context:
            prompt += f"\n\nContext:\n{context}"

        return prompt

    def _parse_plan_response(self, response: str) -> List[Task]:
        """
        Parse the LLM response into Task objects.

        Args:
            response: The LLM response text

        Returns:
            List of Task objects
        """
        import uuid
        import re

        tasks = []
        lines = response.strip().split('\n')

        current_task = None
        task_num = 0

        for line in lines:
            line = line.strip()

            # Match task header
            task_match = re.match(r'Task (\d+): (.+)', line)
            if task_match:
                if current_task:
                    tasks.append(current_task)

                task_num = int(task_match.group(1))
                current_task = Task(
                    id=str(uuid.uuid4()),
                    description=task_match.group(2),
                    dependencies=[]
                )
                continue

            # Match dependencies
            dep_match = re.match(r'Dependencies: (.+)', line, re.IGNORECASE)
            if dep_match and current_task:
                deps = dep_match.group(1).strip().lower()
                if deps != "none":
                    # Convert task numbers to IDs (will be resolved later)
                    current_task.dependencies = deps.split(', ')
                continue

            # Match complexity
            comp_match = re.match(r'Complexity: (.+)', line, re.IGNORECASE)
            if comp_match and current_task:
                comp_str = comp_match.group(1).strip().lower()
                try:
                    current_task.complexity = TaskComplexity(comp_str)
                except ValueError:
                    current_task.complexity = TaskComplexity.MEDIUM
                continue

            # Match estimated time
            time_match = re.match(r'Estimated Time: (\d+)', line, re.IGNORECASE)
            if time_match and current_task:
                current_task.estimated_time = int(time_match.group(1))
                continue

            # Match agent type
            agent_match = re.match(r'Agent: (.+)', line, re.IGNORECASE)
            if agent_match and current_task:
                current_task.agent_type = agent_match.group(1).strip().lower()
                continue

        # Add the last task
        if current_task:
            tasks.append(current_task)

        # Resolve dependencies (convert task numbers to IDs)
        task_map = {i + 1: task.id for i, task in enumerate(tasks)}
        for task in tasks:
            resolved_deps = []
            for dep in task.dependencies:
                try:
                    dep_num = int(dep)
                    if dep_num in task_map:
                        resolved_deps.append(task_map[dep_num])
                except ValueError:
                    pass
            task.dependencies = resolved_deps

        return tasks

    def refine_plan(self, plan: Plan, feedback: str) -> Plan:
        """
        Refine an existing plan based on feedback.

        Args:
            plan: The existing plan
            feedback: User feedback on the plan

        Returns:
            A refined Plan object
        """
        # Build refinement prompt
        system_prompt = self._get_planning_prompt()
        user_prompt = f"""Current Plan:
Goal: {plan.goal}

Tasks:
{self._format_tasks_for_prompt(plan.tasks)}

Feedback:
{feedback}

Please refine the plan based on the feedback. Maintain the same format."""

        # Get refined plan from LLM
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )

        # Parse the refined plan
        tasks = self._parse_plan_response(response.content)

        # Update the plan
        plan.tasks = tasks
        plan.updated_at = datetime.now()

        return plan

    def _format_tasks_for_prompt(self, tasks: List[Task]) -> str:
        """Format tasks for the prompt."""
        task_map = {task.id: i + 1 for i, task in enumerate(tasks)}
        output = []

        for i, task in enumerate(tasks):
            output.append(f"Task {i + 1}: {task.description}")
            if task.dependencies:
                dep_nums = [task_map[dep] for dep in task.dependencies if dep in task_map]
                output.append(f"  Dependencies: {', '.join(map(str, dep_nums))}")
            output.append(f"  Complexity: {task.complexity.value}")
            output.append(f"  Agent: {task.agent_type or 'auto'}")

        return '\n'.join(output)
