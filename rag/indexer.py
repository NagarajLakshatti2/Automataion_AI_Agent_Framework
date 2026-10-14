"""
Codebase indexer for RAG - indexes code files for vector search.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.settings import settings
from core.tools import CodeParser


class CodebaseIndexer:
    """Indexes codebase for RAG-based retrieval."""

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize the codebase indexer.

        Args:
            project_root: Root directory of the project to index
        """
        self.project_root = Path(project_root) if project_root else Path(settings.AI_PROJECT_ROOT)
        self.code_parser = CodeParser()
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

        # File extensions to index
        self.code_extensions = [
            ".py", ".java", ".js", ".jsx", ".ts", ".tsx",
            ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php",
            ".swift", ".kt", ".scala", ".cs",
        ]

        # Directories to skip
        self.skip_dirs = {
            ".git", "__pycache__", "node_modules", "venv", "env",
            ".venv", "dist", "build", ".pytest_cache", ".idea",
            ".vscode", "target", "bin", "obj",
        }

    def index_codebase(self) -> List[Dict[str, Any]]:
        """
        Index the entire codebase.

        Returns:
            List of indexed chunks with metadata
        """
        chunks = []

        for file_path in self.project_root.rglob("*"):
            if self._should_index_file(file_path):
                file_chunks = self._index_file(file_path)
                chunks.extend(file_chunks)

        return chunks

    def _should_index_file(self, file_path: Path) -> bool:
        """
        Check if a file should be indexed.

        Args:
            file_path: Path to the file

        Returns:
            True if file should be indexed
        """
        # Skip directories
        if not file_path.is_file():
            return False

        # Skip files in skip directories
        for part in file_path.parts:
            if part in self.skip_dirs:
                return False

        # Check file extension
        if file_path.suffix.lower() not in self.code_extensions:
            return False

        return True

    def _index_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Index a single file.

        Args:
            file_path: Path to the file

        Returns:
            List of chunks from the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            language = self.code_parser.detect_language(str(file_path))

            # Parse code structure
            structure = self.code_parser.parse_file(str(file_path))

            # Chunk the content
            chunks = self._chunk_content(content, str(file_path), language, structure)

            return chunks

        except (UnicodeDecodeError, IOError):
            return []

    def _chunk_content(
        self,
        content: str,
        file_path: str,
        language: str,
        structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Chunk content into smaller pieces for embedding.

        Args:
            content: File content
            file_path: Path to the file
            language: Programming language
            structure: Parsed code structure

        Returns:
            List of chunks with metadata
        """
        chunks = []

        # Split content into chunks
        lines = content.split('\n')
        num_lines = len(lines)

        for i in range(0, num_lines, self.chunk_size - self.chunk_overlap):
            chunk_lines = lines[i:i + self.chunk_size]
            chunk_content = '\n'.join(chunk_lines)

            # Get context from structure
            chunk_metadata = {
                "file_path": file_path,
                "language": language,
                "start_line": i + 1,
                "end_line": min(i + self.chunk_size, num_lines),
                "content": chunk_content,
            }

            # Add function/class context if available
            if "functions" in structure:
                chunk_metadata["functions"] = structure["functions"]
            if "classes" in structure:
                chunk_metadata["classes"] = structure["classes"]

            chunks.append(chunk_metadata)

        return chunks

    def index_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Index a specific file.

        Args:
            file_path: Path to the file

        Returns:
            List of chunks from the file
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return self._index_file(path)

    def get_files_to_index(self) -> List[str]:
        """
        Get list of files that should be indexed.

        Returns:
            List of file paths
        """
        files = []

        for file_path in self.project_root.rglob("*"):
            if self._should_index_file(file_path):
                files.append(str(file_path))

        return files
