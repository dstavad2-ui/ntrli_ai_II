# ============================================================================
# NTRLI' AI - TOOL REGISTRY
# ============================================================================
"""
Central registry for execution tools.

BEHAVIORAL LAW: No tool may be used unless it is explicitly registered here.
"""

from typing import Dict, Protocol, Any


class Tool(Protocol):
    """Protocol defining the interface for all tools."""
    name: str

    def run(self, payload: dict) -> dict:
        """Execute the tool with given payload."""
        ...


_TOOLS: Dict[str, Tool] = {}


def register_tool(tool: Tool) -> Tool:
    """
    Register a tool in the registry.

    Args:
        tool: Tool instance to register

    Returns:
        The registered tool (for chaining)
    """
    _TOOLS[tool.name] = tool
    return tool


def get(name: str) -> Tool:
    """
    Get a tool by name.

    Args:
        name: The tool name

    Returns:
        The tool instance

    Raises:
        KeyError: If tool is not registered
    """
    if name not in _TOOLS:
        available = ", ".join(_TOOLS.keys()) or "none"
        raise KeyError(f"Unknown tool: {name}. Available: {available}")
    return _TOOLS[name]


def list_tools() -> list[str]:
    """Return list of all registered tool names."""
    return list(_TOOLS.keys())


def is_registered(name: str) -> bool:
    """Check if a tool is registered."""
    return name in _TOOLS
