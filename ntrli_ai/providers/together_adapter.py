# ============================================================================
# NTRLI' AI - TOGETHER AI PROVIDER (HIGH PERFORMANCE)
# ============================================================================
"""
Together AI API Provider

Models: 200+ open-source LLMs, Llama 3.3, Qwen2.5, Mixtral
Best for: Sub-100ms latency, batch inference, cost optimization
Pricing: $0.20-$0.80 per 1M tokens (20% lower than competitors)
Performance: 3.5x faster inference, 2.3x faster training
"""

from .registry import register
from .base import LLMProvider


@register("together")
class TogetherProvider(LLMProvider):
    """Together AI provider - high performance, cost-effective."""

    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        """
        Initialize Together AI provider.

        Args:
            api_key: Together API key
            model: Model to use (default: Llama-3.3-70B-Instruct)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the Together client."""
        if self._client is None:
            from together import Together
            self._client = Together(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Together AI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content or ""
