# ============================================================================
# NTRLI' AI - INTELLIGENT MULTI-PROVIDER ROUTER
# ============================================================================
"""
Intelligent router for multi-provider LLM orchestration.

Supports multiple strategies:
- FASTEST: Prioritize speed (Groq, Together)
- CHEAPEST: Prioritize cost (DeepSeek, Gemini)
- SMARTEST: Prioritize quality (Claude, GPT-4)
- CONSENSUS: Multi-provider voting
- FALLBACK: Try providers in order until success
"""

from typing import Dict, List
from .base import LLMProvider


class RouterStrategy:
    """Available routing strategies."""
    FASTEST = "fastest"        # Groq for speed
    CHEAPEST = "cheapest"      # DeepSeek/Gemini for cost
    SMARTEST = "smartest"      # Claude/GPT-4 for quality
    CONSENSUS = "consensus"    # Multi-provider voting
    FALLBACK = "fallback"      # Try in order until success


class Router:
    """
    Intelligent multi-provider router.

    Routes requests to LLM providers based on strategy.
    """

    def __init__(self, providers: Dict[str, LLMProvider]):
        """
        Initialize router with available providers.

        Args:
            providers: Dictionary mapping provider names to instances
        """
        self.providers = providers
        self.primary = list(providers.keys())[0] if providers else None

        # Provider rankings by category (from web research benchmarks)
        self.rankings = {
            "speed": ["groq", "together", "gemini", "openai", "claude"],
            "cost": ["deepseek", "gemini", "together", "huggingface", "groq"],
            "quality": ["claude", "openai", "gemini", "mistral", "cohere"],
            "coding": ["claude", "openai", "deepseek", "mistral", "groq"]
        }

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0,
        strategy: str = RouterStrategy.FALLBACK
    ) -> Dict[str, str]:
        """
        Generate from providers based on strategy.

        Args:
            prompt: The input prompt
            temperature: Sampling temperature
            strategy: Routing strategy to use

        Returns:
            Dictionary mapping provider names to their outputs
        """
        results = {}

        if strategy == RouterStrategy.CONSENSUS:
            # Use top 3 available providers and return all results
            count = 0
            for name in self._get_provider_order(RouterStrategy.SMARTEST):
                if name in self.providers and count < 3:
                    try:
                        results[name] = self.providers[name].generate(prompt, temperature)
                        count += 1
                    except Exception as e:
                        results[name] = f"ERROR: {e}"

        elif strategy == RouterStrategy.FALLBACK:
            # Try providers in order until success
            for name, provider in self.providers.items():
                try:
                    result = provider.generate(prompt, temperature)
                    results[name] = result
                    break  # Success, stop trying
                except Exception as e:
                    results[name] = f"ERROR: {e}"
                    continue

        else:
            # Single provider strategies (fastest, cheapest, smartest)
            provider_order = self._get_provider_order(strategy)
            for name in provider_order:
                if name in self.providers:
                    try:
                        results[name] = self.providers[name].generate(prompt, temperature)
                        break  # Use first available
                    except Exception:
                        continue

        return results

    def _get_provider_order(self, strategy: str) -> List[str]:
        """Get provider order based on strategy."""
        if strategy == RouterStrategy.FASTEST:
            return self.rankings["speed"]
        elif strategy == RouterStrategy.CHEAPEST:
            return self.rankings["cost"]
        elif strategy == RouterStrategy.SMARTEST:
            return self.rankings["quality"]
        else:
            return list(self.providers.keys())

    def generate_primary(self, prompt: str, temperature: float = 0.0) -> str:
        """Generate from primary provider only."""
        if not self.primary:
            raise RuntimeError("No providers configured")
        return self.providers[self.primary].generate(prompt, temperature)

    def get_available_providers(self) -> List[str]:
        """Return list of available provider names."""
        return list(self.providers.keys())
