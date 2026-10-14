"""
Google AI Studio LLM provider implementation.
Uses Google's Generative AI API for cloud-based LLM inference.
"""
import requests
import json
from typing import Dict, List, Optional, Iterator, Any
from .base import BaseLLMProvider, Message, LLMResponse


class GoogleProvider(BaseLLMProvider):
    """Google AI Studio LLM provider for cloud inference."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Google AI Studio provider.

        Args:
            config: Configuration dict with 'api_key' and 'model' keys
        """
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

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
        # Convert Message objects to Google's format
        # Google AI uses "user" and "model" roles, and system instruction is separate
        system_instruction = None
        contents = []

        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            else:
                role = "user" if msg.role == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg.content}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
            }
        }

        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens

        url = f"{self.base_url}?key={self.api_key}"

        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120
            )
            response.raise_for_status()

            data = response.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]

            usage = data.get("usageMetadata", {})

            return LLMResponse(
                content=content,
                model=self.model,
                finish_reason=data["candidates"][0].get("finishReason"),
                usage={
                    "prompt_tokens": usage.get("promptTokenCount", 0),
                    "completion_tokens": usage.get("candidatesTokenCount", 0),
                    "total_tokens": usage.get("totalTokenCount", 0),
                },
                metadata={"raw_response": data}
            )

        except requests.exceptions.RequestException as e:
            raise Exception(f"Google AI Studio API error: {str(e)}")

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
        # Convert Message objects to Google's format
        system_instruction = None
        contents = []

        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            else:
                role = "user" if msg.role == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg.content}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
            }
        }

        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens

        # Use streamGenerateContent endpoint
        stream_url = self.base_url.replace("generateContent", "streamGenerateContent")
        url = f"{stream_url}?key={self.api_key}&alt=sse"

        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                stream=True,
                timeout=120
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        try:
                            data = json.loads(data_str)
                            content = data["candidates"][0]["content"]["parts"][0].get("text", "")
                            if content:
                                yield content
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue

        except requests.exceptions.RequestException as e:
            raise Exception(f"Google AI Studio streaming error: {str(e)}")

    def validate_config(self) -> bool:
        """
        Validate the Google AI Studio configuration.

        Returns:
            True if configuration is valid
        """
        if not super().validate_config():
            return False

        if not self.api_key:
            return False

        return True
