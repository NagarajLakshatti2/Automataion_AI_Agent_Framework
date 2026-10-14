"""
Test runner tools for executing and analyzing tests.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess
import json


class TestRunner:
    """Test runner tool."""

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize test runner.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()

    def run_pytest(
        self,
        test_path: Optional[str] = None,
        verbose: bool = True,
        coverage: bool = False
    ) -> Dict[str, Any]:
        """
        Run pytest tests.

        Args:
            test_path: Specific test file or directory (if None, runs all tests)
            verbose: Whether to show verbose output
            coverage: Whether to generate coverage report

        Returns:
            Dictionary with test results
        """
        command = ["pytest"]
        if verbose:
            command.append("-v")
        if coverage:
            command.extend(["--cov", "--cov-report=term-missing"])
        if test_path:
            command.append(test_path)

        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )

            return self._parse_pytest_output(result)

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timed out",
                "output": "",
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "pytest not found",
                "output": "",
            }

    def _parse_pytest_output(self, result: subprocess.CompletedProcess) -> Dict[str, Any]:
        """Parse pytest output."""
        output = result.stdout + result.stderr

        # Parse summary
        lines = output.split('\n')
        summary = {}

        for line in lines:
            if "passed" in line.lower() or "failed" in line.lower():
                parts = line.split()
                for part in parts:
                    if "passed" in part:
                        try:
                            summary["passed"] = int(part.split("=")[1])
                        except (IndexError, ValueError):
                            pass
                    elif "failed" in part:
                        try:
                            summary["failed"] = int(part.split("=")[1])
                        except (IndexError, ValueError):
                            pass

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "output": output,
            "summary": summary,
        }

    def run_unittest(
        self,
        test_path: Optional[str] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run unittest tests.

        Args:
            test_path: Specific test file or directory
            verbose: Whether to show verbose output

        Returns:
            Dictionary with test results
        """
        command = ["python", "-m", "unittest"]
        if verbose:
            command.append("-v")
        if test_path:
            command.append(test_path)

        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "output": result.stdout + result.stderr,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timed out",
                "output": "",
            }

    def discover_tests(self, test_dir: str = "tests") -> List[str]:
        """
        Discover test files in a directory.

        Args:
            test_dir: Directory to search for tests

        Returns:
            List of test file paths
        """
        test_path = self.project_root / test_dir

        if not test_path.exists():
            return []

        test_files = []

        for pattern in ["test_*.py", "*_test.py"]:
            test_files.extend(test_path.rglob(pattern))

        return [str(f.relative_to(self.project_root)) for f in test_files]

    def generate_test_report(self, test_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable test report.

        Args:
            test_results: Test results dictionary

        Returns:
            Formatted test report
        """
        if not test_results.get("success"):
            report = "Test Run: FAILED\n"
        else:
            report = "Test Run: PASSED\n"

        report += "=" * 50 + "\n"

        if "summary" in test_results:
            summary = test_results["summary"]
            report += f"Passed: {summary.get('passed', 0)}\n"
            report += f"Failed: {summary.get('failed', 0)}\n"

        if "output" in test_results:
            report += "\nOutput:\n"
            report += test_results["output"]

        return report

    def run_specific_test(self, test_file: str, test_function: str) -> Dict[str, Any]:
        """
        Run a specific test function.

        Args:
            test_file: Test file path
            test_function: Test function name

        Returns:
            Dictionary with test results
        """
        command = ["pytest", f"{test_file}::{test_function}", "-v"]

        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )

            return self._parse_pytest_output(result)

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timed out",
                "output": "",
            }
