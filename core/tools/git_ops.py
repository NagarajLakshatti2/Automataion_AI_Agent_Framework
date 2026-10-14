"""
Git operations tools for managing version control.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess


class GitOperations:
    """Git operations tool."""

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize git operations.

        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self._validate_repo()

    def _validate_repo(self):
        """Validate that the path is a git repository."""
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def _run_git_command(self, command: List[str]) -> str:
        """
        Run a git command and return the output.

        Args:
            command: Git command as list of arguments

        Returns:
            Command output as string

        Raises:
            subprocess.CalledProcessError: If command fails
        """
        result = subprocess.run(
            ["git"] + command,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def get_status(self) -> Dict[str, Any]:
        """
        Get git repository status.

        Returns:
            Dictionary with status information
        """
        try:
            # Get branch name
            branch = self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

            # Get status
            status_output = self._run_git_command(["status", "--porcelain"])

            # Parse status
            staged = []
            modified = []
            untracked = []

            for line in status_output.split('\n'):
                if not line:
                    continue

                status_code = line[:2]
                file_path = line[3:]

                if status_code[0] in ['M', 'A', 'D', 'R']:
                    staged.append(file_path)
                if status_code[1] in ['M', 'D']:
                    modified.append(file_path)
                if status_code == '??':
                    untracked.append(file_path)

            return {
                "branch": branch,
                "staged": staged,
                "modified": modified,
                "untracked": untracked,
                "has_changes": bool(staged or modified or untracked),
            }

        except subprocess.CalledProcessError as e:
            return {
                "error": str(e),
                "branch": "unknown",
                "staged": [],
                "modified": [],
                "untracked": [],
                "has_changes": False,
            }

    def get_diff(self, file_path: Optional[str] = None, staged: bool = False) -> str:
        """
        Get git diff.

        Args:
            file_path: Optional specific file to diff
            staged: Whether to show staged changes

        Returns:
            Diff output as string
        """
        command = ["diff"]
        if staged:
            command.append("--staged")
        if file_path:
            command.append(file_path)

        try:
            return self._run_git_command(command)
        except subprocess.CalledProcessError:
            return ""

    def commit(
        self,
        message: str,
        files: Optional[List[str]] = None,
        add_all: bool = False
    ) -> str:
        """
        Commit changes.

        Args:
            message: Commit message
            files: Specific files to commit (if None, commits staged files)
            add_all: Whether to add all changes before committing

        Returns:
            Commit hash
        """
        if add_all:
            self._run_git_command(["add", "."])
        elif files:
            for file in files:
                self._run_git_command(["add", file])

        self._run_git_command(["commit", "-m", message])

        return self._run_git_command(["rev-parse", "HEAD"])

    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get commit history.

        Args:
            limit: Maximum number of commits to return

        Returns:
            List of commit information dictionaries
        """
        format_str = "%H|%an|%ae|%ad|%s"
        command = ["log", f"--format={format_str}", f"-{limit}"]

        try:
            output = self._run_git_command(command)
            commits = []

            for line in output.split('\n'):
                if not line:
                    continue

                parts = line.split('|', 4)
                if len(parts) == 5:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4],
                    })

            return commits

        except subprocess.CalledProcessError:
            return []

    def create_branch(self, branch_name: str, checkout: bool = True) -> str:
        """
        Create a new branch.

        Args:
            branch_name: Name of the new branch
            checkout: Whether to checkout the new branch

        Returns:
            Name of the created branch
        """
        command = ["branch"]
        if checkout:
            command = ["checkout", "-b"]

        command.append(branch_name)
        self._run_git_command(command)

        return branch_name

    def switch_branch(self, branch_name: str) -> str:
        """
        Switch to a branch.

        Args:
            branch_name: Name of the branch to switch to

        Returns:
            Name of the current branch
        """
        self._run_git_command(["checkout", branch_name])
        return self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

    def list_branches(self) -> Dict[str, List[str]]:
        """
        List all branches.

        Returns:
            Dictionary with 'local' and 'remote' branch lists
        """
        try:
            local = self._run_git_command(["branch", "--format=%(refname:short)"]).split('\n')
            remote = self._run_git_command(["branch", "-r", "--format=%(refname:short)"]).split('\n')

            return {
                "local": [b for b in local if b],
                "remote": [b for b in remote if b],
            }

        except subprocess.CalledProcessError:
            return {"local": [], "remote": []}

    def generate_commit_message(self, changes: str) -> str:
        """
        Generate a commit message from changes description.

        Args:
            changes: Description of changes

        Returns:
            Generated commit message
        """
        # This is a simple implementation
        # In a full implementation, this would use an LLM to generate better messages
        if "add" in changes.lower():
            prefix = "feat"
        elif "fix" in changes.lower() or "bug" in changes.lower():
            prefix = "fix"
        elif "refactor" in changes.lower():
            prefix = "refactor"
        elif "test" in changes.lower():
            prefix = "test"
        elif "docs" in changes.lower():
            prefix = "docs"
        else:
            prefix = "chore"

        return f"{prefix}: {changes[:50]}"

    def get_remote_info(self) -> Dict[str, Any]:
        """
        Get remote repository information.

        Returns:
            Dictionary with remote information
        """
        try:
            remotes = self._run_git_command(["remote", "-v"]).split('\n')
            remote_info = {}

            for line in remotes:
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    url = parts[1]
                    remote_info[name] = url

            return remote_info

        except subprocess.CalledProcessError:
            return {}

    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> str:
        """
        Pull changes from remote.

        Args:
            remote: Remote name
            branch: Branch name (if None, uses current branch)

        Returns:
            Pull output
        """
        command = ["pull", remote]
        if branch:
            command.append(branch)

        return self._run_git_command(command)

    def push(self, remote: str = "origin", branch: Optional[str] = None) -> str:
        """
        Push changes to remote.

        Args:
            remote: Remote name
            branch: Branch name (if None, uses current branch)

        Returns:
            Push output
        """
        command = ["push", remote]
        if branch:
            command.append(branch)

        return self._run_git_command(command)
