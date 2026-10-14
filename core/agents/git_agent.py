"""
Git Operations Agent for managing version control.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts
from core.tools import GitOperations
from config.settings import settings


class GitAgent:
    """Agent for git operations."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the git agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.git_ops = GitOperations(settings.AI_PROJECT_ROOT)
        self.description = "Performs git operations (status, commit, branch, etc.)"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a git operation task.

        Args:
            task_description: Description of git operation
            context: Additional context

        Returns:
            Operation result
        """
        # Parse the task to determine the operation
        task_lower = task_description.lower()

        if "status" in task_lower:
            return self._get_status()
        elif "commit" in task_lower:
            return self._commit(context)
        elif "branch" in task_lower:
            return self._manage_branch(context)
        elif "history" in task_lower or "log" in task_lower:
            return self._get_history(context)
        elif "diff" in task_lower:
            return self._get_diff(context)
        else:
            # Use LLM to interpret the task
            return self._interpret_task(task_description, context)

    def _get_status(self) -> str:
        """Get git status."""
        try:
            status = self.git_ops.get_status()
            output = f"Branch: {status['branch']}\n\n"

            if status['staged']:
                output += "Staged changes:\n"
                for file in status['staged']:
                    output += f"  {file}\n"

            if status['modified']:
                output += "\nModified files:\n"
                for file in status['modified']:
                    output += f"  {file}\n"

            if status['untracked']:
                output += "\nUntracked files:\n"
                for file in status['untracked']:
                    output += f"  {file}\n"

            if not status['has_changes']:
                output += "Working directory clean"

            return output
        except Exception as e:
            return f"Error getting git status: {str(e)}"

    def _commit(self, context: Dict[str, Any]) -> str:
        """Commit changes."""
        message = context.get("message", "Update")
        files = context.get("files")
        add_all = context.get("add_all", True)

        try:
            commit_hash = self.git_ops.commit(message, files, add_all)
            return f"Committed successfully: {commit_hash}"
        except Exception as e:
            return f"Error committing: {str(e)}"

    def _manage_branch(self, context: Dict[str, Any]) -> str:
        """Manage branches."""
        action = context.get("action", "list")
        branch_name = context.get("branch_name")

        try:
            if action == "list":
                branches = self.git_ops.list_branches()
                output = "Local branches:\n"
                for branch in branches['local']:
                    output += f"  {branch}\n"
                output += "\nRemote branches:\n"
                for branch in branches['remote']:
                    output += f"  {branch}\n"
                return output
            elif action == "create" and branch_name:
                return self.git_ops.create_branch(branch_name)
            elif action == "switch" and branch_name:
                return self.git_ops.switch_branch(branch_name)
            else:
                return "Invalid branch operation"
        except Exception as e:
            return f"Error managing branch: {str(e)}"

    def _get_history(self, context: Dict[str, Any]) -> str:
        """Get commit history."""
        limit = context.get("limit", 10)

        try:
            history = self.git_ops.get_history(limit)
            output = f"Last {len(history)} commits:\n\n"

            for commit in history:
                output += f"{commit['hash'][:8]} - {commit['message']}\n"
                output += f"  Author: {commit['author']} <{commit['email']}>\n"
                output += f"  Date: {commit['date']}\n\n"

            return output
        except Exception as e:
            return f"Error getting history: {str(e)}"

    def _get_diff(self, context: Dict[str, Any]) -> str:
        """Get git diff."""
        file_path = context.get("file_path")
        staged = context.get("staged", False)

        try:
            diff = self.git_ops.get_diff(file_path, staged)
            if diff:
                return f"Diff:\n\n{diff}"
            else:
                return "No changes to show"
        except Exception as e:
            return f"Error getting diff: {str(e)}"

    def _interpret_task(self, task_description: str, context: Dict[str, Any]) -> str:
        """Use LLM to interpret complex git operations."""
        system_prompt = Prompts.get_prompt("git_agent")

        user_prompt = f"""Interpret the following git operation task and provide the result:

Task: {task_description}

Context: {context}

Available operations:
- get_status()
- commit(message, files, add_all)
- create_branch(branch_name)
- switch_branch(branch_name)
- list_branches()
- get_history(limit)
- get_diff(file_path, staged)

Please provide the appropriate operation and its result."""

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )

        return response.content
