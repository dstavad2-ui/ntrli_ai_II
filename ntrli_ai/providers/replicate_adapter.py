# ============================================================================
# NTRLI' AI - REPLICATE PROVIDER (OPEN SOURCE MODELS)
# ============================================================================
"""
Replicate API Provider (Open Source Models)

Models: Meta Llama 3.3, Qwen2.5, Mistral, FLUX, Stable Diffusion
Best for: Open source deployment, custom fine-tuned models
Pricing: Pay-per-use, typically $0.0001-$0.001 per second
"""

from .registry import register
from .base import LLMProvider


@register("replicate")
class ReplicateProvider(LLMProvider):
    """Replicate provider for open source models."""

    def __init__(self, api_key: str, model: str = "meta/meta-llama-3.3-70b-instruct"):
        """
        Initialize Replicate provider.

        Args:
            api_key: Replicate API token
            model: Model to use (default: meta-llama-3.3-70b-instruct)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-load the Replicate client."""
        if self._client is None:
            import replicate
            self._client = replicate.Client(api_token=self.api_key)
        return self._client

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate text using Replicate API."""
        output = self.client.run(
            self.model,
            input={
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": 4096
            }
        )
        # Replicate returns an iterator
        return "".join(output)
