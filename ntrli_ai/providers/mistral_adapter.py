# ============================================================================
# NTRLI' AI - MISTRAL AI PROVIDER
# ============================================================================
"""
Mistral AI API Provider

Models: mistral-large-latest, mistral-medium, codestral
Best for: European deployment, code generation, cost-efficiency
Pricing: $2-$8 per 1M tokens
"""

from .registry import register
from .base import LLMProvider


@register("mistral")
class MistralProvider(LLMProvider):
    """Mistral AI provider."""

    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        """
        Initialize Mistral provider.

        Args:
            api_key: Mistral API key
            model: Model to use (default: mistral-large-latest)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the Mistral client."""
        if self._client is None:
            from mistralai import Mistral
            self._client = Mistral(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Mistral API."""
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content or ""
