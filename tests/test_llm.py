"""
Tests for LLM providers.
"""
import pytest
from core.llm import get_llm_provider, Message, LLMResponse
from config.settings import settings


class TestLLMProviders:
    """Test LLM provider implementations."""

    def test_get_llm_provider(self):
        """Test getting an LLM provider."""
        provider = get_llm_provider()
        assert provider is not None
        assert provider.get_model_name() is not None

    def test_ollama_provider_initialization(self):
        """Test Ollama provider initialization."""
        from core.llm.ollama_provider import OllamaProvider

        config = {
            "model": "qwen2.5-coder:7b",
            "url": "http://localhost:11434/api/chat"
        }
        provider = OllamaProvider(config)
        assert provider.model == "qwen2.5-coder:7b"
        assert provider.url == "http://localhost:11434/api/chat"

    def test_openrouter_provider_initialization(self):
        """Test OpenRouter provider initialization."""
        from core.llm.openrouter_provider import OpenRouterProvider

        config = {
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "api_key": "test_key"
        }
        provider = OpenRouterProvider(config)
        assert provider.model == "nvidia/nemotron-3-super-120b-a12b:free"
        assert provider.api_key == "test_key"

    def test_google_provider_initialization(self):
        """Test Google AI Studio provider initialization."""
        from core.llm.google_provider import GoogleProvider

        config = {
            "model": "gemini-pro",
            "api_key": "test_key"
        }
        provider = GoogleProvider(config)
        assert provider.model == "gemini-pro"
        assert provider.api_key == "test_key"

    def test_message_creation(self):
        """Test Message dataclass."""
        message = Message(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"
        assert message.metadata is None

    def test_message_with_metadata(self):
        """Test Message with metadata."""
        metadata = {"key": "value"}
        message = Message(role="assistant", content="Hi", metadata=metadata)
        assert message.metadata == metadata

    def test_llm_response_creation(self):
        """Test LLMResponse dataclass."""
        response = LLMResponse(
            content="Test response",
            model="test-model"
        )
        assert response.content == "Test response"
        assert response.model == "test-model"
        assert response.finish_reason is None

    def test_llm_response_with_usage(self):
        """Test LLMResponse with usage info."""
        usage = {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
        response = LLMResponse(
            content="Test",
            model="test",
            usage=usage
        )
        assert response.usage == usage

    @pytest.mark.skipif(
        not settings.OPENROUTER_API_KEY,
        reason="OPENROUTER_API_KEY not set"
    )
    def test_openrouter_validate_config(self):
        """Test OpenRouter config validation."""
        from core.llm.openrouter_provider import OpenRouterProvider

        config = settings.get_llm_config()
        if config["provider"] == "openrouter":
            provider = OpenRouterProvider(config)
            assert provider.validate_config() is True

    @pytest.mark.skipif(
        not settings.GOOGLE_AI_STUDIO_KEY,
        reason="GOOGLE_AI_STUDIO_KEY not set"
    )
    def test_google_validate_config(self):
        """Test Google provider config validation."""
        from core.llm.google_provider import GoogleProvider

        config = settings.get_llm_config()
        if config["provider"] == "google":
            provider = GoogleProvider(config)
            assert provider.validate_config() is True

    def test_ollama_validate_config_no_connection(self):
        """Test Ollama config validation without connection."""
        from core.llm.ollama_provider import OllamaProvider

        config = {
            "model": "test-model",
            "url": "http://localhost:9999/api/chat"  # Invalid URL
        }
        provider = OllamaProvider(config)
        # Should fail validation due to no connection
        assert provider.validate_config() is False

    def test_provider_name(self):
        """Test getting provider name."""
        from core.llm.ollama_provider import OllamaProvider

        config = {"model": "test", "url": "http://localhost:11434/api/chat"}
        provider = OllamaProvider(config)
        assert provider.get_provider_name() == "ollama"

    def test_base_provider_validate_config_no_model(self):
        """Test base provider validation without model."""
        from core.llm.ollama_provider import OllamaProvider

        config = {"model": "", "url": "http://localhost:11434/api/chat"}
        provider = OllamaProvider(config)
        assert provider.validate_config() is False
