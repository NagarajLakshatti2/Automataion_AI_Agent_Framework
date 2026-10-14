"""
Search tools for finding code and symbols in the codebase.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from .code_parser import CodeParser


class SearchTool:
    """Search tool for finding code and symbols."""

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize search tool.

        Args:
            project_root: Root directory to search in
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.code_parser = CodeParser()

    def search_by_keyword(
        self,
        keyword: str,
        file_pattern: str = "*",
        case_sensitive: bool = False,
        include_content: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search for files containing a keyword.

        Args:
            keyword: Keyword to search for
            file_pattern: File pattern to match (e.g., "*.py")
            case_sensitive: Whether search is case sensitive
            include_content: Whether to include matching lines

        Returns:
            List of search results
        """
        results = []
        keyword_re = keyword if case_sensitive else keyword.lower()

        for file_path in self.project_root.rglob(file_pattern):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    matches = []
                    for i, line in enumerate(lines, 1):
                        line_content = line if case_sensitive else line.lower()
                        if keyword_re in line_content:
                            matches.append({
                                "line_number": i,
                                "content": line.strip(),
                            })

                    if matches:
                        result = {
                            "file": str(file_path.relative_to(self.project_root)),
                            "file_path": str(file_path),
                            "match_count": len(matches),
                        }

                        if include_content:
                            result["matches"] = matches

                        results.append(result)

                except (UnicodeDecodeError, IOError):
                    continue

        return results

    def search_by_regex(
        self,
        pattern: str,
        file_pattern: str = "*",
        flags: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search using regular expression.

        Args:
            pattern: Regular expression pattern
            file_pattern: File pattern to match
            flags: Regex flags

        Returns:
            List of search results
        """
        results = []
        regex = re.compile(pattern, flags)

        for file_path in self.project_root.rglob(file_pattern):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    matches = []
                    for i, line in enumerate(lines, 1):
                        match = regex.search(line)
                        if match:
                            matches.append({
                                "line_number": i,
                                "content": line.strip(),
                                "match": match.group(),
                                "start": match.start(),
                                "end": match.end(),
                            })

                    if matches:
                        results.append({
                            "file": str(file_path.relative_to(self.project_root)),
                            "file_path": str(file_path),
                            "match_count": len(matches),
                            "matches": matches,
                        })

                except (UnicodeDecodeError, IOError):
                    continue

        return results

    def search_function(self, function_name: str) -> List[Dict[str, Any]]:
        """
        Search for function definitions.

        Args:
            function_name: Name of the function to search for

        Returns:
            List of function definitions
        """
        results = []

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                language = self.code_parser.detect_language(str(file_path))
                if not language:
                    continue

                try:
                    structure = self.code_parser.parse_file(str(file_path))
                    functions = self.code_parser.extract_functions(
                        open(file_path).read(),
                        language
                    )

                    for func in functions:
                        if func["name"] == function_name:
                            results.append({
                                "file": str(file_path.relative_to(self.project_root)),
                                "file_path": str(file_path),
                                "language": language,
                                "function": func,
                            })

                except (UnicodeDecodeError, IOError):
                    continue

        return results

    def search_class(self, class_name: str) -> List[Dict[str, Any]]:
        """
        Search for class definitions.

        Args:
            class_name: Name of the class to search for

        Returns:
            List of class definitions
        """
        results = []

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                language = self.code_parser.detect_language(str(file_path))
                if not language:
                    continue

                try:
                    structure = self.code_parser.parse_file(str(file_path))
                    classes = self.code_parser.extract_classes(
                        open(file_path).read(),
                        language
                    )

                    for cls in classes:
                        if cls["name"] == class_name:
                            results.append({
                                "file": str(file_path.relative_to(self.project_root)),
                                "file_path": str(file_path),
                                "language": language,
                                "class": cls,
                            })

                except (UnicodeDecodeError, IOError):
                    continue

        return results

    def search_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Search for any symbol (function, class, variable).

        Args:
            symbol: Symbol name to search for

        Returns:
            List of symbol occurrences
        """
        results = []

        # Search functions
        results.extend(self.search_function(symbol))

        # Search classes
        results.extend(self.search_class(symbol))

        # Search variable definitions (simple regex)
        pattern = rf'\b{re.escape(symbol)}\s*='
        regex_results = self.search_by_regex(pattern, "*")
        for result in regex_results:
            for match in result["matches"]:
                results.append({
                    "file": result["file"],
                    "file_path": result["file_path"],
                    "type": "variable",
                    "line_number": match["line_number"],
                    "content": match["content"],
                })

        return results

    def find_references(self, symbol: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Find references to a symbol in a specific file.

        Args:
            symbol: Symbol name
            file_path: File to search in

        Returns:
            List of references
        """
        results = []
        path = Path(file_path)

        if not path.exists():
            return results

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                # Simple reference check (symbol appears in code)
                if symbol in line:
                    results.append({
                        "line_number": i,
                        "content": line.strip(),
                    })

        except (UnicodeDecodeError, IOError):
            pass

        return results

    def search_imports(self, module_name: str) -> List[Dict[str, Any]]:
        """
        Search for imports of a specific module.

        Args:
            module_name: Module name to search for

        Returns:
            List of import statements
        """
        results = []

        # Search for "import module" and "from module import"
        patterns = [
            rf'import\s+{re.escape(module_name)}',
            rf'from\s+{re.escape(module_name)}\s+import',
        ]

        for pattern in patterns:
            regex_results = self.search_by_regex(pattern, "*.py")
            for result in regex_results:
                for match in result["matches"]:
                    results.append({
                        "file": result["file"],
                        "file_path": result["file_path"],
                        "line_number": match["line_number"],
                        "content": match["content"],
                    })

        return results

    def get_file_structure(self, file_path: str) -> Dict[str, Any]:
        """
        Get the structure of a file (functions, classes, imports).

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file structure
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            structure = self.code_parser.parse_file(str(path))
            structure["file"] = str(path.relative_to(self.project_root))
            structure["file_path"] = str(path)
            structure["language"] = self.code_parser.detect_language(str(path))

            return structure

        except Exception as e:
            return {
                "error": str(e),
                "file": str(path.relative_to(self.project_root)),
            }
