"""
Context retriever for RAG - retrieves relevant code context for LLM queries.
"""
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from config.settings import settings
from .vector_store import VectorStore
from .indexer import CodebaseIndexer


class ContextRetriever:
    """Retrieves relevant code context using vector search."""

    def __init__(self, vector_store: Optional[VectorStore] = None):
        """
        Initialize the context retriever.

        Args:
            vector_store: Optional vector store instance
        """
        self.vector_store = vector_store or VectorStore()
        self.indexer = CodebaseIndexer()

        # Load embedding model
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def retrieve_context(
        self,
        query: str,
        n_results: int = 5,
        filter_language: Optional[str] = None
    ) -> str:
        """
        Retrieve relevant code context for a query.

        Args:
            query: Query text
            n_results: Number of results to retrieve
            filter_language: Optional language filter

        Returns:
            Formatted context string
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)

        # Build filter
        where = None
        if filter_language:
            where = {"language": filter_language}

        # Query vector store
        results = self.vector_store.query(
            query_text=query,
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            where=where
        )

        # Format results
        context = self._format_results(results)

        return context

    def _format_results(self, results: Dict[str, Any]) -> str:
        """
        Format query results into a context string.

        Args:
            results: Query results from vector store

        Returns:
            Formatted context string
        """
        if not results or not results['documents']:
            return "No relevant code context found."

        context_parts = []

        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            context_parts.append(f"--- Context {i + 1} ---")
            context_parts.append(f"File: {metadata['file_path']}")
            context_parts.append(f"Lines: {metadata['start_line']}-{metadata['end_line']}")
            context_parts.append(f"Language: {metadata['language']}")
            context_parts.append("\nCode:")
            context_parts.append(doc)
            context_parts.append("")

        return "\n".join(context_parts)

    def index_and_store(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Index codebase and store embeddings.

        Args:
            file_path: Optional specific file to index (if None, indexes entire codebase)

        Returns:
            Dictionary with indexing statistics
        """
        # Index codebase
        if file_path:
            chunks = self.indexer.index_file(file_path)
        else:
            chunks = self.indexer.index_codebase()

        if not chunks:
            return {
                "success": False,
                "message": "No chunks to index",
                "chunk_count": 0,
            }

        # Generate embeddings
        texts = [chunk['content'] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)

        # Store in vector database
        self.vector_store.add_documents(chunks, embeddings.tolist())

        return {
            "success": True,
            "message": f"Indexed {len(chunks)} chunks",
            "chunk_count": len(chunks),
        }

    def refresh_index(self) -> Dict[str, Any]:
        """
        Refresh the entire index by clearing and re-indexing.

        Returns:
            Dictionary with refresh statistics
        """
        # Clear existing collection
        self.vector_store.clear_collection()

        # Re-index
        return self.index_and_store()

    def get_relevant_files(self, query: str, n_results: int = 10) -> List[str]:
        """
        Get list of relevant files for a query.

        Args:
            query: Query text
            n_results: Number of results

        Returns:
            List of file paths
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)

        # Query vector store
        results = self.vector_store.query(
            query_text=query,
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )

        # Extract unique file paths
        file_paths = set()
        for metadata in results['metadatas'][0]:
            file_paths.add(metadata['file_path'])

        return list(file_paths)

    def search_code(
        self,
        query: str,
        file_path: Optional[str] = None,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for code matching a query.

        Args:
            query: Query text
            file_path: Optional file path to restrict search
            n_results: Number of results

        Returns:
            List of search results
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)

        # Build filter
        where = None
        if file_path:
            where = {"file_path": file_path}

        # Query vector store
        results = self.vector_store.query(
            query_text=query,
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            where=where
        )

        # Format results
        search_results = []
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            search_results.append({
                "rank": i + 1,
                "file_path": metadata['file_path'],
                "lines": f"{metadata['start_line']}-{metadata['end_line']}",
                "language": metadata['language'],
                "content": doc,
            })

        return search_results
