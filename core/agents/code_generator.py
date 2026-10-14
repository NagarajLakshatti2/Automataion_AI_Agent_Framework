"""
Code Generation Agent for generating code from natural language.
"""
from typing import Dict, Any, Optional
from core.llm import BaseLLMProvider, Message
from config.prompts import Prompts
from config.settings import settings


class CodeGeneratorAgent:
    """Agent for generating code from natural language descriptions."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the code generator agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.description = "Generates code from natural language descriptions"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a code generation task.

        Args:
            task_description: Description of code to generate
            context: Additional context (language, style, etc.)

        Returns:
            Generated code
        """
        # Extract language from context or infer from task
        language = context.get("language", self._infer_language(task_description))

        # Build the prompt
        system_prompt = Prompts.get_prompt("code_generator")
        language_specific = Prompts.get_language_specific_prompt(language)

        if language_specific:
            system_prompt += "\n\n" + language_specific

        user_prompt = f"""Generate code for the following task:

Task: {task_description}

Language: {language}

Please provide:
1. The complete, runnable code
2. Brief explanation of the implementation
3. Any necessary imports
4. Error handling where appropriate
"""

        # Add context if available
        if context.get("existing_code"):
            user_prompt += f"\n\nExisting Code Context:\n{context['existing_code']}"

        if context.get("requirements"):
            user_prompt += f"\n\nRequirements:\n{context['requirements']}"

        # Generate code
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )

        return response.content

    def _infer_language(self, task_description: str) -> str:
        """
        Infer the programming language from task description.

        Args:
            task_description: Task description

        Returns:
            Language name
        """
        task_lower = task_description.lower()

        # Simple keyword matching
        language_keywords = {
            "python": ["python", "py", "django", "flask", "fastapi"],
            "javascript": ["javascript", "js", "node", "express", "react"],
            "typescript": ["typescript", "ts", "angular"],
            "java": ["java", "spring", "maven", "gradle"],
            "cpp": ["c++", "cpp", "qt"],
            "c": ["c language", "c code"],
            "go": ["golang", "go"],
            "rust": ["rust", "cargo"],
            "ruby": ["ruby", "rails"],
            "php": ["php", "laravel"],
        }

        for language, keywords in language_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                return language

        # Default to Python
        return "python"
