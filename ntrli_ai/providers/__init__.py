# ============================================================================
# NTRLI' AI - PROVIDERS MODULE
# ============================================================================
"""
Multi-provider LLM abstraction layer.

Supports:
- OpenAI (GPT-4o, o1)
- Anthropic Claude (Claude 4, Claude 3.5)
- Google Gemini
- Groq (fastest inference)
- Mistral AI
- Together AI
- Replicate
- DeepSeek
- Hugging Face
- Cohere
"""

from .base import LLMProvider
from .registry import register, get_provider, list_providers
from .router import Router, RouterStrategy

__all__ = [
    "LLMProvider",
    "register",
    "get_provider",
    "list_providers",
    "Router",
    "RouterStrategy",
]
