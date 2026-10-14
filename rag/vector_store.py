"""
Vector store using ChromaDB for storing and retrieving code embeddings.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from config.settings import settings


class VectorStore:
    """Vector store using ChromaDB for code embeddings."""

    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_dir = Path(persist_directory or settings.CHROMA_PERSIST_DIR)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.collection_name = settings.CHROMA_COLLECTION_NAME

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        """Get existing collection or create new one."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
            return collection
        except:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Codebase embeddings"}
            )

    def add_documents(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: Optional[List[List[float]]] = None
    ) -> None:
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of chunk dictionaries with content and metadata
            embeddings: Optional pre-computed embeddings
        """
        if not chunks:
            return

        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{chunk['file_path']}:{chunk['start_line']}-{chunk['end_line']}"
            ids.append(chunk_id)
            documents.append(chunk['content'])

            metadata = {
                "file_path": chunk['file_path'],
                "language": chunk.get('language', 'unknown'),
                "start_line": chunk['start_line'],
                "end_line": chunk['end_line'],
            }

            # Add additional metadata if available
            if 'functions' in chunk:
                metadata['functions'] = str(chunk['functions'])
            if 'classes' in chunk:
                metadata['classes'] = str(chunk['classes'])

            metadatas.append(metadata)

        # Add to collection
        if embeddings:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
        else:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    def query(
        self,
        query_text: str,
        query_embeddings: Optional[List[float]] = None,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the vector store for similar documents.

        Args:
            query_text: Query text
            query_embeddings: Optional pre-computed query embeddings
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            Query results with documents and metadata
        """
        if query_embeddings:
            results = self.collection.query(
                query_embeddings=[query_embeddings],
                n_results=n_results,
                where=where
            )
        else:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )

        return results

    def delete_by_file(self, file_path: str) -> None:
        """
        Delete all documents from a specific file.

        Args:
            file_path: Path to the file
        """
        # Get all documents with this file path
        results = self.collection.get(
            where={"file_path": file_path}
        )

        if results['ids']:
            self.collection.delete(ids=results['ids'])

    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Codebase embeddings"}
            )
        except Exception as e:
            print(f"Error clearing collection: {str(e)}")

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": str(self.persist_dir),
            }
        except Exception as e:
            return {
                "error": str(e),
                "collection_name": self.collection_name,
            }

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents in the collection.

        Returns:
            List of all documents with metadata
        """
        try:
            results = self.collection.get()
            documents = []

            for i in range(len(results['ids'])):
                documents.append({
                    "id": results['ids'][i],
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i],
                })

            return documents
        except Exception as e:
            print(f"Error getting documents: {str(e)}")
            return []
