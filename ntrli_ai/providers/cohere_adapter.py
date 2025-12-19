# ============================================================================
# NTRLI' AI - COHERE PROVIDER (ENTERPRISE RAG)
# ============================================================================
"""
Cohere API Provider

Models: command-r-plus, command-r, embed-v3
Best for: RAG applications, semantic search, embeddings
Pricing: $3-$15 per 1M tokens
"""

from .registry import register
from .base import LLMProvider


@register("cohere")
class CohereProvider(LLMProvider):
    """Cohere provider for enterprise RAG applications."""

    def __init__(self, api_key: str, model: str = "command-r-plus"):
        """
        Initialize Cohere provider.

        Args:
            api_key: Cohere API key
            model: Model to use (default: command-r-plus)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the Cohere client."""
        if self._client is None:
            import cohere
            self._client = cohere.Client(self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Cohere API."""
        response = self.client.chat(
            model=self.model,
            message=prompt,
            temperature=temperature
        )
        return response.text
