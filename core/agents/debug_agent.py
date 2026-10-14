"""
Debugging Agent for analyzing and fixing code issues.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts
from core.tools import Debugger


class DebugAgent:
    """Agent for debugging code."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the debug agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.debugger = Debugger()
        self.description = "Analyzes errors and provides debugging strategies"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a debugging task.

        Args:
            task_description: Description of debugging task
            context: Additional context (error_message, stack_trace, code, etc.)

        Returns:
            Debugging analysis and suggestions
        """
        # Parse the task to determine the operation
        task_lower = task_description.lower()

        if "error" in task_lower or "exception" in task_lower:
            return self._analyze_error(context)
        elif "breakpoint" in task_lower:
            return self._suggest_breakpoints(context)
        else:
            # Use LLM to interpret the task
            return self._interpret_task(task_description, context)

    def _analyze_error(self, context: Dict[str, Any]) -> str:
        """Analyze an error."""
        error_message = context.get("error_message", "")
        stack_trace = context.get("stack_trace")

        if not error_message:
            return "Error: error_message not provided in context"

        try:
            analysis = self.debugger.analyze_error(error_message, stack_trace)
            strategy = self.debugger.generate_debugging_strategy(analysis)

            return strategy
        except Exception as e:
            return f"Error analyzing error: {str(e)}"

    def _suggest_breakpoints(self, context: Dict[str, Any]) -> str:
        """Suggest breakpoints for debugging."""
        code = context.get("code", "")
        error_location = context.get("error_location")

        if not code:
            return "Error: code not provided in context"

        try:
            breakpoints = self.debugger.suggest_breakpoints(code, error_location)

            output = "Suggested breakpoints:\n\n"
            for bp in breakpoints:
                output += f"Line {bp['line']}: {bp['reason']}\n"
                output += f"  Code: {bp['code']}\n\n"

            return output
        except Exception as e:
            return f"Error suggesting breakpoints: {str(e)}"

    def _interpret_task(self, task_description: str, context: Dict[str, Any]) -> str:
        """Use LLM to interpret complex debugging tasks."""
        system_prompt = Prompts.get_prompt("debug_agent")

        user_prompt = f"""Interpret the following debugging task and provide the result:

Task: {task_description}

Context: {context}

Available operations:
- analyze_error(error_message, stack_trace)
- suggest_breakpoints(code, error_location)
- generate_debugging_strategy(error_analysis)

Please provide the appropriate operation and its result."""

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )

        return response.content
