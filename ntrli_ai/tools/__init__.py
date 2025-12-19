# ============================================================================
# NTRLI' AI - TOOLS MODULE
# ============================================================================
"""
Explicit, registered tools for NTRLI' AI execution.

All tools must be:
1. Explicitly registered
2. Have a defined name
3. Implement the run() method
4. Return structured results
"""

from .registry import register_tool, get, list_tools

# Import tools to trigger registration
from . import web_research
from . import code_validate
from . import code_execute
from . import run_tests
from . import code_generate
from . import artifact_write
from . import notebook_query
from . import github_writeback

__all__ = [
    "register_tool",
    "get",
    "list_tools",
]
