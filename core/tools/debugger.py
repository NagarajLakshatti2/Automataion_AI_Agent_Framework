"""
Debugging tools for analyzing and fixing code issues.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import re


class Debugger:
    """Debugging tool for analyzing errors and providing fixes."""

    def __init__(self):
        """Initialize the debugger."""
        self.error_patterns = {
            "SyntaxError": r"SyntaxError:\s*(.+)",
            "NameError": r"NameError:\s*name\s+'(\w+)'\s+is\s+not\s+defined",
            "TypeError": r"TypeError:\s*(.+)",
            "ValueError": r"ValueError:\s*(.+)",
            "AttributeError": r"AttributeError:\s*'(\w+)'\s+object\s+has\s+no\s+attribute\s+'(\w+)'",
            "KeyError": r"KeyError:\s*['\"](.+)['\"]",
            "IndexError": r"IndexError:\s*(.+)",
            "ImportError": r"ImportError:\s*(.+)",
            "ZeroDivisionError": r"ZeroDivisionError:\s*(.+)",
        }

    def analyze_error(self, error_message: str, stack_trace: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze an error message and provide diagnosis.

        Args:
            error_message: The error message
            stack_trace: Optional stack trace

        Returns:
            Dictionary with error analysis
        """
        analysis = {
            "error_type": None,
            "error_message": error_message,
            "suggested_fixes": [],
            "likely_causes": [],
            "context": {},
        }

        # Detect error type
        for error_type, pattern in self.error_patterns.items():
            match = re.search(pattern, error_message)
            if match:
                analysis["error_type"] = error_type
                analysis["context"]["match"] = match.groups()
                break

        # Provide suggestions based on error type
        if analysis["error_type"]:
            analysis["suggested_fixes"] = self._get_fixes_for_error(
                analysis["error_type"],
                analysis["context"].get("match", [])
            )
            analysis["likely_causes"] = self._get_causes_for_error(analysis["error_type"])

        # Analyze stack trace if provided
        if stack_trace:
            analysis["stack_analysis"] = self._analyze_stack_trace(stack_trace)

        return analysis

    def _get_fixes_for_error(self, error_type: str, match_groups: tuple) -> List[str]:
        """Get suggested fixes for a specific error type."""
        fixes = []

        if error_type == "NameError":
            variable_name = match_groups[0] if match_groups else "variable"
            fixes = [
                f"Check if '{variable_name}' is defined before use",
                f"Look for typos in '{variable_name}'",
                f"Ensure '{variable_name}' is in the correct scope",
                f"Import the module or define '{variable_name}' if needed",
            ]

        elif error_type == "TypeError":
            fixes = [
                "Check the types of the operands",
                "Ensure you're using the correct operation for the data types",
                "Add type conversion if needed (e.g., str(), int())",
                "Review the function signature and arguments",
            ]

        elif error_type == "AttributeError":
            obj = match_groups[0] if match_groups else "object"
            attr = match_groups[1] if len(match_groups) > 1 else "attribute"
            fixes = [
                f"Check if '{obj}' has the attribute '{attr}'",
                f"Verify the object type and available methods",
                f"Check for typos in the attribute name '{attr}'",
                f"Ensure the object is properly initialized",
            ]

        elif error_type == "KeyError":
            key = match_groups[0] if match_groups else "key"
            fixes = [
                f"Check if '{key}' exists in the dictionary",
                f"Use dict.get('{key}', default) to provide a default value",
                f"Check for case sensitivity or whitespace in '{key}'",
                f"Print the dictionary keys to debug",
            ]

        elif error_type == "IndexError":
            fixes = [
                "Check if the index is within the valid range",
                "Verify the length of the list/array before accessing",
                "Use try-except to handle index errors gracefully",
                "Check for off-by-one errors",
            ]

        elif error_type == "ImportError":
            fixes = [
                "Check if the module is installed (pip install module_name)",
                "Verify the module name is correct",
                "Check if the module is in the Python path",
                "Ensure you're using the correct Python environment",
            ]

        elif error_type == "SyntaxError":
            fixes = [
                "Check for missing colons, parentheses, or brackets",
                "Verify proper indentation",
                "Check for mismatched quotes",
                "Review the line number mentioned in the error",
            ]

        elif error_type == "ZeroDivisionError":
            fixes = [
                "Check if the denominator is zero before division",
                "Add a conditional check for division by zero",
                "Use try-except to handle ZeroDivisionError",
                "Consider using a default value or alternative logic",
            ]

        return fixes

    def _get_causes_for_error(self, error_type: str) -> List[str]:
        """Get likely causes for a specific error type."""
        causes = {
            "NameError": [
                "Variable used before definition",
                "Typo in variable name",
                "Variable out of scope",
                "Missing import",
            ],
            "TypeError": [
                "Incompatible types in operation",
                "Wrong number of arguments",
                "Calling non-callable object",
            ],
            "AttributeError": [
                "Incorrect object type",
                "Attribute doesn't exist",
                "Object not properly initialized",
            ],
            "KeyError": [
                "Key doesn't exist in dictionary",
                "Case mismatch",
                "Whitespace in key",
            ],
            "IndexError": [
                "Index out of range",
                "Empty list/array",
                "Off-by-one error",
            ],
            "ImportError": [
                "Module not installed",
                "Wrong module name",
                "Module not in Python path",
            ],
            "SyntaxError": [
                "Missing punctuation",
                "Incorrect indentation",
                "Invalid syntax for language",
            ],
            "ZeroDivisionError": [
                "Division by zero",
                "Empty list causing division",
            ],
        }

        return causes.get(error_type, ["Unknown cause"])

    def _analyze_stack_trace(self, stack_trace: str) -> Dict[str, Any]:
        """
        Analyze a stack trace.

        Args:
            stack_trace: Stack trace string

        Returns:
            Dictionary with stack trace analysis
        """
        lines = stack_trace.split('\n')
        frames = []

        for line in lines:
            # Match stack trace frame pattern
            # File "file.py", line X, in function
            match = re.search(r'File\s+"([^"]+)",\s+line\s+(\d+),\s+in\s+(\w+)', line)
            if match:
                frames.append({
                    "file": match.group(1),
                    "line": int(match.group(2)),
                    "function": match.group(3),
                })

        return {
            "frames": frames,
            "frame_count": len(frames),
            "deepest_frame": frames[-1] if frames else None,
        }

    def suggest_breakpoints(self, code: str, error_location: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Suggest strategic breakpoints for debugging.

        Args:
            code: Code to analyze
            error_location: Optional location of the error

        Returns:
            List of suggested breakpoint locations
        """
        breakpoints = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            # Suggest breakpoints at:
            # 1. Function definitions
            if re.match(r'def\s+\w+\s*\(', line):
                breakpoints.append({
                    "line": i,
                    "reason": "Function entry",
                    "code": line.strip(),
                })

            # 2. Loop conditions
            if re.match(r'\s*(for|while)\s+', line):
                breakpoints.append({
                    "line": i,
                    "reason": "Loop start",
                    "code": line.strip(),
                })

            # 3. Conditional statements
            if re.match(r'\s*if\s+', line):
                breakpoints.append({
                    "line": i,
                    "reason": "Conditional check",
                    "code": line.strip(),
                })

            # 4. Before error location
            if error_location:
                # This is a simplified check
                pass

        return breakpoints

    def generate_debugging_strategy(self, error_analysis: Dict[str, Any]) -> str:
        """
        Generate a debugging strategy based on error analysis.

        Args:
            error_analysis: Error analysis dictionary

        Returns:
            Debugging strategy as string
        """
        strategy = f"Debugging Strategy for {error_analysis.get('error_type', 'Unknown Error')}\n"
        strategy += "=" * 60 + "\n\n"

        if error_analysis.get("likely_causes"):
            strategy += "Likely Causes:\n"
            for cause in error_analysis["likely_causes"]:
                strategy += f"  - {cause}\n"
            strategy += "\n"

        if error_analysis.get("suggested_fixes"):
            strategy += "Suggested Fixes:\n"
            for fix in error_analysis["suggested_fixes"]:
                strategy += f"  1. {fix}\n"
            strategy += "\n"

        if "stack_analysis" in error_analysis:
            stack = error_analysis["stack_analysis"]
            if stack.get("deepest_frame"):
                frame = stack["deepest_frame"]
                strategy += f"Error Location:\n"
                strategy += f"  File: {frame['file']}\n"
                strategy += f"  Line: {frame['line']}\n"
                strategy += f"  Function: {frame['function']}\n"
                strategy += "\n"

        strategy += "Next Steps:\n"
        strategy += "  1. Review the error location in the code\n"
        strategy += "  2. Add print statements or breakpoints to inspect variables\n"
        strategy += "  3. Apply the suggested fixes one at a time\n"
        strategy += "  4. Test after each fix to verify the issue is resolved\n"

        return strategy
