"""
Code Conversion Agent for converting code between languages.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts


class CodeConverterAgent:
    """Agent for converting code between programming languages."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the code converter agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.description = "Converts code between different programming languages"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a code conversion task.

        Args:
            task_description: Description of conversion task
            context: Additional context (source_code, source_language, target_language)

        Returns:
            Converted code
        """
        # Extract source and target languages from context
        source_code = context.get("source_code", "")
        source_language = context.get("source_language", self._infer_language(source_code))
        target_language = context.get("target_language", self._infer_target_language(task_description))

        # Build the prompt
        system_prompt = Prompts.get_prompt("code_converter")

        user_prompt = f"""Convert the following code from {source_language} to {target_language}:

Source Code:
```{source_language}
{source_code}
```

Please provide:
1. The converted code in {target_language}
2. Explanation of any significant changes
3. Notes on language-specific adaptations
4. Any imports or dependencies needed
"""

        # Generate converted code
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )

        return response.content

    def _infer_language(self, code: str) -> str:
        """Infer language from code."""
        if "def " in code or "import " in code:
            return "python"
        elif "public class" in code or "public static void" in code:
            return "java"
        elif "function " in code or "const " in code or "let " in code:
            return "javascript"
        elif "interface " in code or ": " in code and " => " in code:
            return "typescript"
        elif "#include" in code:
            return "cpp"
        return "python"

    def _infer_target_language(self, task_description: str) -> str:
        """Infer target language from task description."""
        task_lower = task_description.lower()

        language_keywords = {
            "python": ["python", "py"],
            "java": ["java"],
            "javascript": ["javascript", "js"],
            "typescript": ["typescript", "ts"],
            "cpp": ["c++", "cpp"],
            "go": ["golang", "go"],
            "rust": ["rust"],
        }

        for language, keywords in language_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                return language

        return "python"
