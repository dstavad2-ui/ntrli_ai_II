# ============================================================================
# NTRLI' AI - ANTHROPIC CLAUDE PROVIDER
# ============================================================================
"""
Anthropic Claude API Provider

Models: claude-4-opus, claude-4-sonnet, claude-3.5-sonnet
Best for: Long context (200K), coding (93.7% accuracy), analysis
Pricing: $3-$15 per 1M input tokens
"""

from .registry import register
from .base import LLMProvider


@register("claude")
class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude provider.

        Args:
            api_key: Anthropic API key
            model: Model to use (default: claude-sonnet-4-20250514)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the Anthropic client."""
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Anthropic API."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
