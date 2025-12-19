# ============================================================================
# NTRLI' AI - HUGGING FACE INFERENCE PROVIDER
# ============================================================================
"""
Hugging Face Inference API Provider

Models: Custom deployed models, open source transformers
Best for: Custom models, research, free tier experimentation
Pricing: FREE tier + Inference Endpoints ($0.60-$4/hr)
"""

import requests
from .registry import register
from .base import LLMProvider


@register("huggingface")
class HuggingFaceProvider(LLMProvider):
    """Hugging Face Inference API provider."""

    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        """
        Initialize Hugging Face provider.

        Args:
            api_key: Hugging Face API key
            model: Model to use (default: Llama-3.3-70B-Instruct)
        """
        self.api_key = api_key
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Hugging Face Inference API."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature if temperature > 0 else 0.01,
                "max_new_tokens": 4096,
                "return_full_text": False
            }
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return ""
