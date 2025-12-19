# ============================================================================
# NTRLI' AI - DEEPSEEK PROVIDER (ULTRA LOW COST)
# ============================================================================
"""
DeepSeek API Provider

Models: deepseek-chat, deepseek-coder
Best for: ULTRA LOW COST ($0.14/1M tokens), budget projects
Pricing: 50-100x cheaper than GPT-4
"""

from .registry import register
from .base import LLMProvider


@register("deepseek")
class DeepSeekProvider(LLMProvider):
    """DeepSeek provider - ultra low cost."""

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        """
        Initialize DeepSeek provider.

        Args:
            api_key: DeepSeek API key
            model: Model to use (default: deepseek-chat)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the OpenAI-compatible client for DeepSeek."""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using DeepSeek API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content or ""
