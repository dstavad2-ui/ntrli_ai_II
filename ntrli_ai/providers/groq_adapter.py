# ============================================================================
# NTRLI' AI - GROQ PROVIDER (FASTEST INFERENCE)
# ============================================================================
"""
Groq LPU Inference API Provider

Models: llama-3.3-70b, mixtral-8x7b, gemma-2-9b
Best for: SPEED (276 tokens/sec), real-time apps, low latency
Pricing: FREE tier available, $0.59/1M tokens production
Benchmark: Fastest AI inference in 2024 (ArtificialAnalysis.ai)
"""

from .registry import register
from .base import LLMProvider


@register("groq")
class GroqProvider(LLMProvider):
    """Groq LPU inference provider - fastest available."""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize Groq provider.

        Args:
            api_key: Groq API key
            model: Model to use (default: llama-3.3-70b-versatile)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the Groq client."""
        if self._client is None:
            from groq import Groq
            self._client = Groq(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Groq API - fastest inference."""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return completion.choices[0].message.content or ""
