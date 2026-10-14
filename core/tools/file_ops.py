"""
File operations tools for reading, writing, and managing files.
"""
from pathlib import Path
from typing import List, Optional, Dict, Any
import os
import shutil
from datetime import datetime


class FileOperations:
    """File operations tool."""

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize file operations.

        Args:
            project_root: Root directory for file operations
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()

    def read_file(self, file_path: str, encoding: Optional[str] = None) -> str:
        """
        Read a file's contents.

        Args:
            file_path: Path to the file (relative to project root or absolute)
            encoding: File encoding (auto-detected if None)

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        path = self._resolve_path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if encoding is None:
            encoding = self._detect_encoding(path)

        with open(path, 'r', encoding=encoding) as f:
            return f.read()

    def write_file(
        self,
        file_path: str,
        content: str,
        encoding: str = 'utf-8',
        create_backup: bool = True
    ) -> str:
        """
        Write content to a file.

        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding
            create_backup: Whether to create a backup before overwriting

        Returns:
            Path to the written file

        Raises:
            IOError: If file cannot be written
        """
        path = self._resolve_path(file_path)

        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup if file exists and backup is requested
        if create_backup and path.exists():
            backup_path = self._create_backup(path)
            return self._write_to_file(path, content, encoding, backup_path)

        return self._write_to_file(path, content, encoding)

    def _write_to_file(
        self,
        path: Path,
        content: str,
        encoding: str,
        backup_path: Optional[Path] = None
    ) -> str:
        """Write content to file."""
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)

        result = str(path)
        if backup_path:
            result += f" (backup: {backup_path})"

        return result

    def _create_backup(self, path: Path) -> Path:
        """Create a backup of a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.parent / f"{path.stem}.backup_{timestamp}{path.suffix}"
        shutil.copy2(path, backup_path)
        return backup_path

    def list_directory(
        self,
        dir_path: str = ".",
        recursive: bool = False,
        include_hidden: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List files and directories.

        Args:
            dir_path: Directory path to list
            recursive: Whether to list recursively
            include_hidden: Whether to include hidden files

        Returns:
            List of file/directory information dictionaries
        """
        path = self._resolve_path(dir_path)

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")

        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        items = []

        if recursive:
            for item in path.rglob("*"):
                if not include_hidden and item.name.startswith("."):
                    continue
                items.append(self._get_file_info(item))
        else:
            for item in path.iterdir():
                if not include_hidden and item.name.startswith("."):
                    continue
                items.append(self._get_file_info(item))

        return items

    def _get_file_info(self, path: Path) -> Dict[str, Any]:
        """Get information about a file or directory."""
        stat = path.stat()

        return {
            "name": path.name,
            "path": str(path),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": path.suffix if path.is_file() else None,
        }

    def create_directory(self, dir_path: str) -> str:
        """
        Create a directory.

        Args:
            dir_path: Path to the directory

        Returns:
            Path to the created directory
        """
        path = self._resolve_path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def delete_file(self, file_path: str, confirm: bool = False) -> bool:
        """
        Delete a file or directory.

        Args:
            file_path: Path to delete
            confirm: Whether deletion is confirmed

        Returns:
            True if deleted, False otherwise

        Raises:
            PermissionError: If not confirmed
        """
        if not confirm:
            raise PermissionError("Deletion must be confirmed")

        path = self._resolve_path(file_path)

        if not path.exists():
            return False

        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)

        return True

    def search_files(
        self,
        pattern: str,
        dir_path: str = ".",
        case_sensitive: bool = False
    ) -> List[str]:
        """
        Search for files matching a pattern.

        Args:
            pattern: File name pattern (supports * and ?)
            dir_path: Directory to search in
            case_sensitive: Whether search is case sensitive

        Returns:
            List of matching file paths
        """
        path = self._resolve_path(dir_path)

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")

        if not case_sensitive:
            pattern = pattern.lower()

        matches = []
        for item in path.rglob("*"):
            name = item.name if case_sensitive else item.name.lower()
            if self._match_pattern(name, pattern):
                matches.append(str(item))

        return matches

    def _match_pattern(self, name: str, pattern: str) -> bool:
        """Check if name matches pattern."""
        import fnmatch
        return fnmatch.fnmatch(name, pattern)

    def _resolve_path(self, file_path: str) -> Path:
        """Resolve a file path relative to project root."""
        path = Path(file_path)

        if not path.is_absolute():
            path = self.project_root / path

        return path.resolve()

    def _detect_encoding(self, path: Path) -> str:
        """Detect file encoding."""
        try:
            import chardet
            with open(path, 'rb') as f:
                raw_data = f.read(1024)
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
        except ImportError:
            # Fallback if chardet is not available
            return 'utf-8'

    def get_file_stats(self, file_path: str) -> Dict[str, Any]:
        """
        Get statistics about a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file statistics
        """
        path = self._resolve_path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        stat = path.stat()

        return {
            "path": str(path),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
        }
