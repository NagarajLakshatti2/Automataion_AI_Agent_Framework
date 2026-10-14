"""
Code Review Agent for analyzing code quality and best practices.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts


class CodeReviewerAgent:
    """Agent for reviewing code quality and best practices."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the code reviewer agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.description = "Reviews code for quality, security, and best practices"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a code review task.

        Args:
            task_description: Description of review task
            context: Additional context (code to review, language, etc.)

        Returns:
            Code review report
        """
        # Extract code from context
        code = context.get("code", "")
        language = context.get("language", "python")

        # Build the prompt
        system_prompt = Prompts.get_prompt("code_reviewer")

        user_prompt = f"""Review the following {language} code:

```{language}
{code}
```

Please provide a comprehensive review including:
1. Potential bugs or logic errors
2. Security vulnerabilities
3. Code quality issues
4. Best practices violations
5. Performance concerns
6. Suggestions for improvement
7. Overall assessment (1-10 scale)
"""

        if task_description:
            user_prompt += f"\n\nSpecific focus: {task_description}"

        # Generate review
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )

        return response.content
