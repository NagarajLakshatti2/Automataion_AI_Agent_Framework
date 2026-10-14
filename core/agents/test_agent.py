"""
Testing Agent for generating and running tests.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts
from core.tools import TestRunner
from config.settings import settings


class TestAgent:
    """Agent for testing operations."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the test agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.test_runner = TestRunner(settings.AI_PROJECT_ROOT)
        self.description = "Generates and runs tests"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a testing task.

        Args:
            task_description: Description of testing task
            context: Additional context (code, test_path, etc.)

        Returns:
            Task result
        """
        # Parse the task to determine the operation
        task_lower = task_description.lower()

        if "run" in task_lower or "execute" in task_lower:
            return self._run_tests(context)
        elif "generate" in task_lower or "create" in task_lower:
            return self._generate_tests(context)
        elif "discover" in task_lower or "find" in task_lower:
            return self._discover_tests(context)
        else:
            # Use LLM to interpret the task
            return self._interpret_task(task_description, context)

    def _run_tests(self, context: Dict[str, Any]) -> str:
        """Run tests."""
        test_path = context.get("test_path")
        framework = context.get("framework", "pytest")

        try:
            if framework == "pytest":
                results = self.test_runner.run_pytest(test_path)
            else:
                results = self.test_runner.run_unittest(test_path)

            report = self.test_runner.generate_test_report(results)
            return report
        except Exception as e:
            return f"Error running tests: {str(e)}"

    def _generate_tests(self, context: Dict[str, Any]) -> str:
        """Generate tests for code."""
        code = context.get("code", "")
        language = context.get("language", "python")

        system_prompt = Prompts.get_prompt("test_agent")

        user_prompt = f"""Generate comprehensive tests for the following {language} code:

```{language}
{code}
```

Please provide:
1. Test cases for all functions/methods
2. Edge case testing
3. Error condition testing
4. Setup and teardown if needed
5. Use appropriate testing framework conventions"""

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )

        return response.content

    def _discover_tests(self, context: Dict[str, Any]) -> str:
        """Discover test files."""
        test_dir = context.get("test_dir", "tests")

        try:
            test_files = self.test_runner.discover_tests(test_dir)
            output = f"Found {len(test_files)} test files:\n\n"

            for test_file in test_files:
                output += f"  {test_file}\n"

            return output
        except Exception as e:
            return f"Error discovering tests: {str(e)}"

    def _interpret_task(self, task_description: str, context: Dict[str, Any]) -> str:
        """Use LLM to interpret complex testing tasks."""
        system_prompt = Prompts.get_prompt("test_agent")

        user_prompt = f"""Interpret the following testing task and provide the result:

Task: {task_description}

Context: {context}

Available operations:
- run_pytest(test_path, verbose, coverage)
- run_unittest(test_path, verbose)
- discover_tests(test_dir)
- generate_test_report(test_results)

Please provide the appropriate operation and its result."""

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )

        return response.content
