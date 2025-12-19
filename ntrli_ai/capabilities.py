# ============================================================================
# NTRLI' AI - CAPABILITY REGISTRY (SELF-KNOWLEDGE)
# ============================================================================
"""
This module defines the capabilities that NTRLI' AI knows it has.
This is how the system maintains strict self-awareness of its limits.

BEHAVIORAL LAW: No execution without verified capabilities.
"""

from typing import Dict, Literal

CapabilityName = Literal[
    "web_research", "notebook_query", "code_generate",
    "code_validate", "code_execute", "run_tests",
    "github_read", "github_write"
]

# The canonical registry of all capabilities
# If a capability is not here, NTRLI' AI cannot use it
CAPABILITIES: Dict[str, bool] = {
    "web_research": True,
    "notebook_query": True,
    "code_generate": True,
    "code_validate": True,
    "code_execute": True,
    "run_tests": True,
    "github_read": True,
    "github_write": True,
    # Action aliases used by planner
    "research": True,
    "artifact_write": True,
    "github_writeback": True,
}


class CapabilityError(RuntimeError):
    """Raised when attempting to use an unavailable capability."""
    pass


def assert_capability(name: str) -> None:
    """
    Assert that a capability is available.

    Args:
        name: The capability name to check

    Raises:
        CapabilityError: If the capability is not available
    """
    if not CAPABILITIES.get(name, False):
        raise CapabilityError(f"Capability not available: {name}")


def list_capabilities() -> list[str]:
    """Return list of all enabled capabilities."""
    return [k for k, v in CAPABILITIES.items() if v]


def disable_capability(name: str) -> None:
    """Disable a capability at runtime."""
    if name in CAPABILITIES:
        CAPABILITIES[name] = False


def enable_capability(name: str) -> None:
    """Enable a capability at runtime."""
    if name in CAPABILITIES:
        CAPABILITIES[name] = True
