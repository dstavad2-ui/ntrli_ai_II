# ============================================================================
# NTRLI' AI - PROVIDER REGISTRY
# ============================================================================
"""
Central registry for LLM providers.

Providers register themselves using the @register decorator.
The system can only use providers that are explicitly registered here.
"""

from typing import Dict, Type, Callable
from .base import LLMProvider

_REGISTRY: Dict[str, Type[LLMProvider]] = {}


def register(name: str) -> Callable[[Type[LLMProvider]], Type[LLMProvider]]:
    """
    Decorator to register an LLM provider.

    Args:
        name: The provider name (e.g., "openai", "claude")

    Returns:
        Decorator function

    Example:
        @register("openai")
        class OpenAIProvider(LLMProvider):
            ...
    """
    def decorator(cls: Type[LLMProvider]) -> Type[LLMProvider]:
        _REGISTRY[name] = cls
        return cls
    return decorator


def get_provider(name: str, **kwargs) -> LLMProvider:
    """
    Get an instance of a registered provider.

    Args:
        name: The provider name
        **kwargs: Arguments to pass to the provider constructor

    Returns:
        Configured provider instance

    Raises:
        ValueError: If provider is not registered
    """
    if name not in _REGISTRY:
        available = ", ".join(_REGISTRY.keys()) or "none"
        raise ValueError(f"Unknown provider: {name}. Available: {available}")
    return _REGISTRY[name](**kwargs)


def list_providers() -> list[str]:
    """Return list of all registered provider names."""
    return list(_REGISTRY.keys())


def is_registered(name: str) -> bool:
    """Check if a provider is registered."""
    return name in _REGISTRY
