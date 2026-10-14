"""
LLM provider initialization and factory.
"""
from .base import BaseLLMProvider, Message, LLMResponse
from .ollama_provider import OllamaProvider
from .openrouter_provider import OpenRouterProvider
from .google_provider import GoogleProvider
from config.settings import settings


def get_llm_provider() -> BaseLLMProvider:
    """
    Get the configured LLM provider.

    Returns:
        An instance of the configured LLM provider

    Raises:
        ValueError: If the provider is not supported
    """
    config = settings.get_llm_config()
    provider_name = config["provider"]

    if provider_name == "ollama":
        return OllamaProvider(config)
    elif provider_name == "openrouter":
        return OpenRouterProvider(config)
    elif provider_name == "google":
        return GoogleProvider(config)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")


__all__ = [
    "BaseLLMProvider",
    "Message",
    "LLMResponse",
    "OllamaProvider",
    "OpenRouterProvider",
    "GoogleProvider",
    "get_llm_provider",
]
