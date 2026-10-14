"""
OpenRouter LLM provider implementation.
Uses OpenRouter API for cloud-based LLM inference with free tier models.
"""
import requests
import json
from typing import Dict, List, Optional, Iterator, Any
from .base import BaseLLMProvider, Message, LLMResponse


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter LLM provider for cloud inference."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenRouter provider.

        Args:
            config: Configuration dict with 'api_key' and 'model' keys
        """
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response for a single prompt.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            LLMResponse object
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return self.chat(messages, temperature, max_tokens, **kwargs)

    def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response for a conversation.

        Args:
            messages: List of Message objects
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            LLMResponse object
        """
        # Convert Message objects to dict format
        openrouter_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        payload = {
            "model": self.model,
            "messages": openrouter_messages,
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jeshlaaiagent.local",
            "X-Title": "JeshlaAIAgent"
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=120
            )
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            usage = data.get("usage", {})

            return LLMResponse(
                content=content,
                model=self.model,
                finish_reason=data["choices"][0].get("finish_reason"),
                usage={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                },
                metadata={"raw_response": data}
            )

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API error: {str(e)}")

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream a response for a single prompt.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Yields:
            Chunks of the generated response
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        yield from self.stream_chat(messages, temperature, max_tokens, **kwargs)

    def stream_chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream a response for a conversation.

        Args:
            messages: List of Message objects
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Yields:
            Chunks of the generated response
        """
        # Convert Message objects to dict format
        openrouter_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        payload = {
            "model": self.model,
            "messages": openrouter_messages,
            "temperature": temperature,
            "stream": True,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jeshlaaiagent.local",
            "X-Title": "JeshlaAIAgent"
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                stream=True,
                timeout=120
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            data = json.loads(data_str)
                            content = data["choices"][0]["delta"].get("content", "")
                            if content:
                                yield content
                        except (json.JSONDecodeError, KeyError):
                            continue

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter streaming error: {str(e)}")

    def validate_config(self) -> bool:
        """
        Validate the OpenRouter configuration.

        Returns:
            True if configuration is valid
        """
        if not super().validate_config():
            return False

        if not self.api_key:
            return False

        return True
