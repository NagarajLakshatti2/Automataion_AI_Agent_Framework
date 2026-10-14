"""
File Operations Agent for reading, writing, and managing files.
"""
from typing import Dict, Any
from core.llm import BaseLLMProvider
from config.prompts import Prompts
from core.tools import FileOperations
from config.settings import settings


class FileAgent:
    """Agent for file operations."""

    def __init__(self, llm: BaseLLMProvider):
        """
        Initialize the file agent.

        Args:
            llm: LLM provider instance
        """
        self.llm = llm
        self.file_ops = FileOperations(settings.AI_PROJECT_ROOT)
        self.description = "Performs file operations (read, write, list, etc.)"

    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Execute a file operation task.

        Args:
            task_description: Description of file operation
            context: Additional context (file_path, content, etc.)

        Returns:
            Operation result
        """
        # Parse the task to determine the operation
        task_lower = task_description.lower()

        if "read" in task_lower:
            return self._read_file(context)
        elif "write" in task_lower or "save" in task_lower:
            return self._write_file(context)
        elif "list" in task_lower or "show" in task_lower:
            return self._list_directory(context)
        elif "create" in task_lower:
            return self._create_directory(context)
        elif "delete" in task_lower:
            return self._delete_file(context)
        else:
            # Use LLM to interpret the task
            return self._interpret_task(task_description, context)

    def _read_file(self, context: Dict[str, Any]) -> str:
        """Read a file."""
        file_path = context.get("file_path")
        if not file_path:
            return "Error: file_path not provided in context"

        try:
            content = self.file_ops.read_file(file_path)
            return f"File content:\n\n{content}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def _write_file(self, context: Dict[str, Any]) -> str:
        """Write to a file."""
        file_path = context.get("file_path")
        content = context.get("content")
        if not file_path or content is None:
            return "Error: file_path or content not provided in context"

        try:
            result = self.file_ops.write_file(file_path, content)
            return f"File written successfully: {result}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def _list_directory(self, context: Dict[str, Any]) -> str:
        """List directory contents."""
        dir_path = context.get("dir_path", ".")
        recursive = context.get("recursive", False)

        try:
            items = self.file_ops.list_directory(dir_path, recursive)
            output = f"Directory listing for {dir_path}:\n\n"

            for item in items:
                icon = "📁" if item["is_dir"] else "📄"
                output += f"{icon} {item['name']}"
                if item["is_dir"]:
                    output += "/"
                output += "\n"

            return output
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    def _create_directory(self, context: Dict[str, Any]) -> str:
        """Create a directory."""
        dir_path = context.get("dir_path")
        if not dir_path:
            return "Error: dir_path not provided in context"

        try:
            result = self.file_ops.create_directory(dir_path)
            return f"Directory created: {result}"
        except Exception as e:
            return f"Error creating directory: {str(e)}"

    def _delete_file(self, context: Dict[str, Any]) -> str:
        """Delete a file or directory."""
        file_path = context.get("file_path")
        if not file_path:
            return "Error: file_path not provided in context"

        try:
            result = self.file_ops.delete_file(file_path, confirm=True)
            return f"File deleted: {result}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"

    def _interpret_task(self, task_description: str, context: Dict[str, Any]) -> str:
        """Use LLM to interpret complex file operations."""
        system_prompt = Prompts.get_prompt("file_agent")

        user_prompt = f"""Interpret the following file operation task and provide the result:

Task: {task_description}

Context: {context}

Available operations:
- read_file(file_path)
- write_file(file_path, content)
- list_directory(dir_path, recursive)
- create_directory(dir_path)
- delete_file(file_path)

Please provide the appropriate operation and its result."""

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )

        return response.content
