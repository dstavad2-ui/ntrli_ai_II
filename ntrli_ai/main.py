#!/usr/bin/env python3
# ============================================================================
# NTRLI' AI - MAIN ENTRY POINT
# ============================================================================
"""
NTRLI' AI - Deterministic, Execution-First Artificial Intelligence System

This is the main entry point for the NTRLI' AI system.
It initializes all providers, sets up the router, and handles execution.

Usage:
    python main.py '<instruction>'

Environment Variables:
    OPENAI_API_KEY      - OpenAI API key (GPT-4o)
    ANTHROPIC_API_KEY   - Anthropic API key (Claude)
    GOOGLE_API_KEY      - Google API key (Gemini)
    GROQ_API_KEY        - Groq API key (fastest inference)
    MISTRAL_API_KEY     - Mistral API key
    TOGETHER_API_KEY    - Together AI API key
    REPLICATE_API_TOKEN - Replicate API token
    DEEPSEEK_API_KEY    - DeepSeek API key
    HUGGINGFACE_API_KEY - Hugging Face API key
    COHERE_API_KEY      - Cohere API key
    ROUTER_STRATEGY     - Router strategy (fastest|cheapest|smartest|consensus|fallback)
    GITHUB_TOKEN        - GitHub token for repository operations
"""

import sys
import json
import os
from typing import Dict

# Import providers to trigger registration
from providers.openai_adapter import OpenAIProvider
from providers.claude_adapter import ClaudeProvider
from providers.gemini_adapter import GeminiProvider
from providers.groq_adapter import GroqProvider
from providers.mistral_adapter import MistralProvider
from providers.together_adapter import TogetherProvider
from providers.replicate_adapter import ReplicateProvider
from providers.deepseek_adapter import DeepSeekProvider
from providers.huggingface_adapter import HuggingFaceProvider
from providers.cohere_adapter import CohereProvider

from providers.registry import get_provider
from providers.router import Router, RouterStrategy
from control_plane import ControlPlane

# Import tools to trigger registration
import tools


def initialize_providers() -> Dict[str, object]:
    """
    Initialize all available providers based on environment variables.

    Returns:
        Dictionary mapping provider names to provider instances
    """
    providers = {}

    # OpenAI (GPT-4o, o1) - Best for general purpose
    if openai_key := os.getenv("OPENAI_API_KEY"):
        try:
            providers["openai"] = get_provider("openai", api_key=openai_key, model="gpt-4o")
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI: {e}", file=sys.stderr)

    # Anthropic Claude - Best for coding (93.7% accuracy)
    if claude_key := os.getenv("ANTHROPIC_API_KEY"):
        try:
            providers["claude"] = get_provider("claude", api_key=claude_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Claude: {e}", file=sys.stderr)

    # Google Gemini - Cheapest premium ($1.25/1M tokens)
    if gemini_key := os.getenv("GOOGLE_API_KEY"):
        try:
            providers["gemini"] = get_provider("gemini", api_key=gemini_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini: {e}", file=sys.stderr)

    # Groq - FASTEST inference (276 tokens/sec)
    if groq_key := os.getenv("GROQ_API_KEY"):
        try:
            providers["groq"] = get_provider("groq", api_key=groq_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Groq: {e}", file=sys.stderr)

    # Mistral AI - European compliance
    if mistral_key := os.getenv("MISTRAL_API_KEY"):
        try:
            providers["mistral"] = get_provider("mistral", api_key=mistral_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Mistral: {e}", file=sys.stderr)

    # Together AI - 3.5x faster, 20% cheaper
    if together_key := os.getenv("TOGETHER_API_KEY"):
        try:
            providers["together"] = get_provider("together", api_key=together_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Together: {e}", file=sys.stderr)

    # Replicate - Open source models
    if replicate_key := os.getenv("REPLICATE_API_TOKEN"):
        try:
            providers["replicate"] = get_provider("replicate", api_key=replicate_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Replicate: {e}", file=sys.stderr)

    # DeepSeek - Ultra low cost ($0.14/1M)
    if deepseek_key := os.getenv("DEEPSEEK_API_KEY"):
        try:
            providers["deepseek"] = get_provider("deepseek", api_key=deepseek_key)
        except Exception as e:
            print(f"Warning: Failed to initialize DeepSeek: {e}", file=sys.stderr)

    # Hugging Face - Custom models, free tier
    if hf_key := os.getenv("HUGGINGFACE_API_KEY"):
        try:
            providers["huggingface"] = get_provider("huggingface", api_key=hf_key)
        except Exception as e:
            print(f"Warning: Failed to initialize HuggingFace: {e}", file=sys.stderr)

    # Cohere - Enterprise RAG
    if cohere_key := os.getenv("COHERE_API_KEY"):
        try:
            providers["cohere"] = get_provider("cohere", api_key=cohere_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Cohere: {e}", file=sys.stderr)

    return providers


def main():
    """Main entry point for NTRLI' AI."""
    # Initialize providers
    providers = initialize_providers()

    if not providers:
        print("ERROR: No API keys configured", file=sys.stderr)
        print("Set at least one of:", file=sys.stderr)
        print("  OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY,", file=sys.stderr)
        print("  GROQ_API_KEY, MISTRAL_API_KEY, TOGETHER_API_KEY,", file=sys.stderr)
        print("  REPLICATE_API_TOKEN, DEEPSEEK_API_KEY,", file=sys.stderr)
        print("  HUGGINGFACE_API_KEY, COHERE_API_KEY", file=sys.stderr)
        sys.exit(1)

    print(f"NTRLI' AI initialized with {len(providers)} provider(s):", file=sys.stderr)
    print(f"  {', '.join(providers.keys())}", file=sys.stderr)

    # Initialize router with configured strategy
    strategy = os.getenv("ROUTER_STRATEGY", RouterStrategy.FALLBACK)
    router = Router(providers)
    print(f"Router strategy: {strategy}", file=sys.stderr)

    # Initialize control plane
    control_plane = ControlPlane(router)

    # Get instruction from command line
    if len(sys.argv) < 2:
        print("Usage: python main.py '<instruction>'", file=sys.stderr)
        print("", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  python main.py 'Research Python best practices'", file=sys.stderr)
        sys.exit(1)

    instruction = sys.argv[1]
    print(f"Executing: {instruction}", file=sys.stderr)

    # Execute
    try:
        result = control_plane.handle({
            "command": "EXECUTE",
            "conversation_id": "cli",
            "instructions": instruction
        })

        # Output result as JSON
        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        error_output = {
            "error": str(e),
            "type": type(e).__name__
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
