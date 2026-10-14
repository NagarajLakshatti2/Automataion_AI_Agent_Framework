"""
Configuration management for JeshlaAIAgent.
Loads environment variables and provides configuration access.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings."""

    # Application Info
    APP_NAME: str = os.getenv("APP_NAME", "JeshlaAIAgent")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # LLM Provider
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")

    # Google AI Studio
    GOOGLE_AI_STUDIO_KEY: Optional[str] = os.getenv("GOOGLE_AI_STUDIO_KEY")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-pro")

    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")

    # Ollama
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

    # Project Root
    AI_PROJECT_ROOT: str = os.getenv("AI_PROJECT_ROOT", os.getcwd())

    # Vector Database (ChromaDB)
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "codebase")

    # RAG Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # Supported Languages
    SUPPORTED_LANGUAGES = [
        "python",
        "java",
        "javascript",
        "typescript",
        "cpp",
        "c",
        "go",
        "rust",
        "ruby",
        "php",
        "swift",
        "kotlin",
        "scala",
        "csharp",
    ]

    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration based on selected provider."""
        provider = cls.LLM_PROVIDER.lower()

        if provider == "ollama":
            return {
                "provider": "ollama",
                "model": cls.OLLAMA_MODEL,
                "url": cls.OLLAMA_URL,
            }
        elif provider == "openrouter":
            if not cls.OPENROUTER_API_KEY:
                raise ValueError("OPENROUTER_API_KEY not set in environment")
            return {
                "provider": "openrouter",
                "model": cls.OPENROUTER_MODEL,
                "api_key": cls.OPENROUTER_API_KEY,
            }
        elif provider == "google":
            if not cls.GOOGLE_AI_STUDIO_KEY:
                raise ValueError("GOOGLE_AI_STUDIO_KEY not set in environment")
            return {
                "provider": "google",
                "model": cls.GOOGLE_MODEL,
                "api_key": cls.GOOGLE_AI_STUDIO_KEY,
            }
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        errors = []

        # Validate LLM provider
        if cls.LLM_PROVIDER not in ["ollama", "openrouter", "google"]:
            errors.append(f"Invalid LLM_PROVIDER: {cls.LLM_PROVIDER}")

        # Validate API keys based on provider
        if cls.LLM_PROVIDER == "openrouter" and not cls.OPENROUTER_API_KEY:
            errors.append("OPENROUTER_API_KEY required when using openrouter")
        if cls.LLM_PROVIDER == "google" and not cls.GOOGLE_AI_STUDIO_KEY:
            errors.append("GOOGLE_AI_STUDIO_KEY required when using google")

        # Validate project root
        if not os.path.exists(cls.AI_PROJECT_ROOT):
            errors.append(f"AI_PROJECT_ROOT does not exist: {cls.AI_PROJECT_ROOT}")

        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False

        return True

    @classmethod
    def get_project_root(cls) -> Path:
        """Get project root as Path object."""
        return Path(cls.AI_PROJECT_ROOT)


# Global settings instance
settings = Settings()
