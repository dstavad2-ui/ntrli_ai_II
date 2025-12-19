# ============================================================================
# NTRLI' AI - GOOGLE GEMINI PROVIDER
# ============================================================================
"""
Google Gemini API Provider

Models: gemini-2.5-pro, gemini-2.5-flash, gemini-exp-1206
Best for: Multimodal (vision/audio), cost ($1.25/1M tokens), speed
Pricing: $1.25-$7 per 1M input tokens (cheapest premium option)
"""

from .registry import register
from .base import LLMProvider


@register("gemini")
class GeminiProvider(LLMProvider):
    """Google Gemini provider."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        Initialize Gemini provider.

        Args:
            api_key: Google API key
            model: Model to use (default: gemini-2.5-flash)
        """
        self.api_key = api_key
        self.model_name = model
        self._model = None

    @property
    def model(self):
        """Lazy-load the Gemini model."""
        if self._model is None:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(self.model_name)
        return self._model

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Gemini API."""
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        return response.text
