# ============================================================================
# NTRLI' AI - NOTEBOOK QUERY TOOL
# ============================================================================
"""
Notebook/knowledge cache query tool.

Queries the local knowledge cache for previously stored information.
"""

from typing import Dict, Any, Optional, List
from .registry import register_tool


class NotebookQuery:
    """Query the knowledge cache."""

    name = "notebook_query"

    def __init__(self):
        self._cache = None

    def set_cache(self, cache) -> None:
        """Inject the knowledge cache module."""
        self._cache = cache

    def run(self, payload: dict) -> dict:
        """
        Query the knowledge cache.

        Args:
            payload: Must contain "topic" to query

        Returns:
            Dictionary with cached data or empty result
        """
        topic = payload.get("topic", "")

        if not topic:
            return {"found": False, "error": "No topic provided", "data": None}

        if not self._cache:
            # Try to import directly
            try:
                from .. import knowledge_cache
                self._cache = knowledge_cache
            except ImportError:
                return {"found": False, "error": "Cache not configured", "data": None}

        try:
            data = self._cache.load(topic)

            if data is not None:
                return {
                    "found": True,
                    "topic": topic,
                    "data": data
                }
            else:
                return {
                    "found": False,
                    "topic": topic,
                    "data": None
                }

        except Exception as e:
            return {
                "found": False,
                "error": str(e),
                "data": None
            }


# Register the tool
register_tool(NotebookQuery())
