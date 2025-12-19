# ============================================================================
# NTRLI' AI - OPENAI PROVIDER (GPT-4, GPT-4o, o1)
# ============================================================================
"""
OpenAI API Provider

Models: GPT-4o, GPT-4-turbo, o1-preview, o1-mini
Best for: General purpose, structured output, reasoning
Pricing: $5-$15 per 1M input tokens
"""

from .registry import register
from .base import LLMProvider


@register("openai")
class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the OpenAI client."""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content or ""
