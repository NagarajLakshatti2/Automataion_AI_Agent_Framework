"""
Agent Orchestrator for coordinating multiple agents.
"""
from typing import Dict, Any, Optional, List
from core.llm import get_llm_provider, Message
from config.prompts import Prompts


class AgentOrchestrator:
    """Orchestrates and coordinates multiple specialized agents."""

    def __init__(self):
        """Initialize the agent orchestrator."""
        self.llm = get_llm_provider()
        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all available agents."""
        from .code_generator import CodeGeneratorAgent
        from .code_converter import CodeConverterAgent
        from .code_reviewer import CodeReviewerAgent
        from .file_agent import FileAgent
        from .git_agent import GitAgent
        from .test_agent import TestAgent
        from .debug_agent import DebugAgent
        from .refactor_agent import RefactorAgent

        self.agents = {
            "code_generator": CodeGeneratorAgent(self.llm),
            "code_converter": CodeConverterAgent(self.llm),
            "code_reviewer": CodeReviewerAgent(self.llm),
            "file_agent": FileAgent(self.llm),
            "git_agent": GitAgent(self.llm),
            "test_agent": TestAgent(self.llm),
            "debug_agent": DebugAgent(self.llm),
            "refactor_agent": RefactorAgent(self.llm),
        }

    def execute_task(
        self,
        agent_type: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a task using a specific agent.

        Args:
            agent_type: Type of agent to use
            task_description: Description of the task
            context: Additional context for the task

        Returns:
            Task result as string
        """
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent = self.agents[agent_type]
        return agent.execute(task_description, context or {})

    def route_task(self, task_description: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Automatically route a task to the appropriate agent.

        Args:
            task_description: Description of the task
            context: Additional context for the task

        Returns:
            Task result as string
        """
        # Use LLM to determine which agent should handle the task
        agent_type = self._determine_agent_type(task_description)
        return self.execute_task(agent_type, task_description, context)

    def _determine_agent_type(self, task_description: str) -> str:
        """
        Determine which agent should handle a task.

        Args:
            task_description: Description of the task

        Returns:
            Agent type string
        """
        # Simple keyword-based routing
        task_lower = task_description.lower()

        routing_rules = {
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
        for agent_type, keywords in routing_rules.items():
            if any(keyword in task_lower for keyword in keywords):
                return agent_type

        # Default to code_generator
        return "code_generator"

    def get_agent_status(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get status of agents.

        Args:
            agent_type: Specific agent type (if None, returns all)

        Returns:
            Dictionary with agent status
        """
        if agent_type:
            if agent_type not in self.agents:
                raise ValueError(f"Unknown agent type: {agent_type}")
            return {
                agent_type: {
                    "available": True,
                    "name": self.agents[agent_type].__class__.__name__,
                }
            }

        return {
            agent_type: {
                "available": True,
                "name": agent.__class__.__name__,
            }
            for agent_type, agent in self.agents.items()
        }

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all available agents.

        Returns:
            List of agent information
        """
        return [
            {
                "type": agent_type,
                "name": agent.__class__.__name__,
                "description": agent.description if hasattr(agent, 'description') else "",
            }
            for agent_type, agent in self.agents.items()
        ]

    def coordinate_agents(
        self,
        task_description: str,
        agent_sequence: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Coordinate multiple agents to complete a complex task.

        Args:
            task_description: Overall task description
            agent_sequence: List of agent types to execute in order
            context: Additional context

        Returns:
            List of results from each agent
        """
        results = []
        current_context = context or {}

        for agent_type in agent_sequence:
            try:
                result = self.execute_task(agent_type, task_description, current_context)
                results.append({
                    "agent": agent_type,
                    "success": True,
                    "result": result,
                })

                # Update context for next agent
                current_context["previous_results"] = results

            except Exception as e:
                results.append({
                    "agent": agent_type,
                    "success": False,
                    "error": str(e),
                })
                break

        return results
