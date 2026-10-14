"""
Code parser utilities for analyzing code structure.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import re


class CodeParser:
    """Code parser for analyzing code structure."""

    def __init__(self):
        """Initialize the code parser."""
        self.language_extensions = {
            "python": [".py"],
            "java": [".java"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "cpp": [".cpp", ".cc", ".cxx"],
            "c": [".c", ".h"],
            "go": [".go"],
            "rust": [".rs"],
            "ruby": [".rb"],
            "php": [".php"],
            "swift": [".swift"],
            "kotlin": [".kt"],
            "scala": [".scala"],
            "csharp": [".cs"],
        }

    def detect_language(self, file_path: str) -> Optional[str]:
        """
        Detect the programming language from file extension.

        Args:
            file_path: Path to the file

        Returns:
            Language name or None if not detected
        """
        path = Path(file_path)
        ext = path.suffix.lower()

        for language, extensions in self.language_extensions.items():
            if ext in extensions:
                return language

        return None

    def parse_python(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code structure.

        Args:
            code: Python code string

        Returns:
            Dictionary with parsed structure
        """
        structure = {
            "functions": [],
            "classes": [],
            "imports": [],
            "docstrings": [],
        }

        # Extract imports
        import_patterns = [
            r'^import\s+([^\n]+)',
            r'^from\s+([^\s]+)\s+import',
        ]
        for pattern in import_patterns:
            for match in re.finditer(pattern, code, re.MULTILINE):
                structure["imports"].append(match.group(1).strip())

        # Extract functions
        func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?\s*:'
        for match in re.finditer(func_pattern, code):
            structure["functions"].append({
                "name": match.group(1),
                "args": match.group(2).strip(),
                "return_type": match.group(3).strip() if match.group(3) else None,
            })

        # Extract classes
        class_pattern = r'class\s+(\w+)\s*(?:\(([^)]+)\))?\s*:'
        for match in re.finditer(class_pattern, code):
            structure["classes"].append({
                "name": match.group(1),
                "inherits": match.group(2).strip() if match.group(2) else None,
            })

        return structure

    def parse_javascript(self, code: str) -> Dict[str, Any]:
        """
        Parse JavaScript code structure.

        Args:
            code: JavaScript code string

        Returns:
            Dictionary with parsed structure
        """
        structure = {
            "functions": [],
            "classes": [],
            "imports": [],
            "variables": [],
        }

        # Extract imports
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
        ]
        for pattern in import_patterns:
            for match in re.finditer(pattern, code):
                structure["imports"].append(match.group(1))

        # Extract functions
        func_patterns = [
            r'function\s+(\w+)\s*\(([^)]*)\)',
            r'const\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>',
            r'(\w+)\s*\(([^)]*)\)\s*{',
        ]
        for pattern in func_patterns:
            for match in re.finditer(pattern, code):
                structure["functions"].append({
                    "name": match.group(1),
                    "args": match.group(2).strip(),
                })

        # Extract classes
        class_pattern = r'class\s+(\w+)\s*(?:extends\s+(\w+))?\s*{'
        for match in re.finditer(class_pattern, code):
            structure["classes"].append({
                "name": match.group(1),
                "extends": match.group(2) if match.group(2) else None,
            })

        return structure

    def parse_java(self, code: str) -> Dict[str, Any]:
        """
        Parse Java code structure.

        Args:
            code: Java code string

        Returns:
            Dictionary with parsed structure
        """
        structure = {
            "classes": [],
            "methods": [],
            "imports": [],
            "packages": [],
        }

        # Extract package
        package_pattern = r'package\s+([^\s;]+);'
        for match in re.finditer(package_pattern, code):
            structure["packages"].append(match.group(1))

        # Extract imports
        import_pattern = r'import\s+([^\s;]+);'
        for match in re.finditer(import_pattern, code):
            structure["imports"].append(match.group(1))

        # Extract classes
        class_pattern = r'(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?'
        for match in re.finditer(class_pattern, code):
            structure["classes"].append({
                "name": match.group(1),
                "extends": match.group(2),
                "implements": match.group(3).split(',') if match.group(3) else [],
            })

        # Extract methods
        method_pattern = r'(?:public|private|protected)?\s*(?:static)?\s*(?:\w+)\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(method_pattern, code):
            structure["methods"].append({
                "name": match.group(1),
                "args": match.group(2).strip(),
            })

        return structure

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a code file and extract its structure.

        Args:
            file_path: Path to the code file

        Returns:
            Dictionary with parsed structure
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()

        language = self.detect_language(file_path)

        if language == "python":
            return self.parse_python(code)
        elif language in ["javascript", "typescript"]:
            return self.parse_javascript(code)
        elif language == "java":
            return self.parse_java(code)
        else:
            # Generic parsing for unsupported languages
            return {
                "language": language,
                "lines": len(code.split('\n')),
                "characters": len(code),
            }

    def extract_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract function definitions from code.

        Args:
            code: Code string
            language: Programming language

        Returns:
            List of function information dictionaries
        """
        if language == "python":
            return self.parse_python(code)["functions"]
        elif language in ["javascript", "typescript"]:
            return self.parse_javascript(code)["functions"]
        elif language == "java":
            return self.parse_java(code)["methods"]
        else:
            return []

    def extract_classes(self, code: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract class definitions from code.

        Args:
            code: Code string
            language: Programming language

        Returns:
            List of class information dictionaries
        """
        if language == "python":
            return self.parse_python(code)["classes"]
        elif language in ["javascript", "typescript"]:
            return self.parse_javascript(code)["classes"]
        elif language == "java":
            return self.parse_java(code)["classes"]
        else:
            return []

    def count_lines_of_code(self, file_path: str) -> Dict[str, int]:
        """
        Count lines of code in a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with line counts
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                comment_lines += 1
            else:
                code_lines += 1

        return {
            "total": total_lines,
            "code": code_lines,
            "comments": comment_lines,
            "blank": blank_lines,
        }
