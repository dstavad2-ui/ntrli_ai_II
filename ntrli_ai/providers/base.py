# ============================================================================
# NTRLI' AI - LLM PROVIDER BASE
# ============================================================================
"""
Abstract base class for all LLM providers.

All providers must implement the generate() method with deterministic
defaults (temperature=0.0) to ensure consistent, reproducible behavior.
"""

from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Base class for all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        """
        Generate text from the LLM.

        Args:
            prompt: The input prompt
            temperature: Sampling temperature (0.0 for deterministic)

        Returns:
            Generated text response
        """
        pass

    def get_model_info(self) -> dict:
        """Return information about the current model configuration."""
        return {
            "provider": self.__class__.__name__,
            "model": getattr(self, "model", "unknown"),
        }
