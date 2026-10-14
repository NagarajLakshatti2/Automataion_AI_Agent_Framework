"""
Refactoring Agent for improving code quality and structure.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts


class RefactorAgent:
    """Agent for code refactoring."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the refactor agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.description = "Identifies and applies code refactoring improvements"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a refactoring task.

        Args:
            task_description: Description of refactoring task
            context: Additional context (code, language, etc.)

        Returns:
            Refactored code and explanation
        """
        # Extract code from context
        code = context.get("code", "")
        language = context.get("language", "python")

        # Build the prompt
        system_prompt = Prompts.get_prompt("refactor_agent")

        user_prompt = f"""Refactor the following {language} code to improve quality and maintainability:

```{language}
{code}
```

Task: {task_description}

Please provide:
1. The refactored code
2. Explanation of improvements made
3. Benefits of the refactoring
4. Any potential risks or considerations
"""

        # Generate refactored code
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )

        return response.content
