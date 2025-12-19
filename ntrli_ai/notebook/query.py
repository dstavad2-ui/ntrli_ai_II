# ============================================================================
# NTRLI' AI - NOTEBOOK QUERY ENGINE
# ============================================================================
"""
Notebook query engine for searching stored knowledge.

Provides simple text-based search across notebook entries.
"""

from typing import List, Dict, Any, Optional
from .store import NotebookStore


class NotebookQueryEngine:
    """
    Query engine for notebook searches.

    Provides text-based search across stored entries.
    """

    def __init__(self, store: NotebookStore):
        """
        Initialize query engine.

        Args:
            store: The notebook store to query
        """
        self.store = store

    def search(
        self,
        query: str,
        entry_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search notebook entries.

        Args:
            query: Search query (simple text match)
            entry_type: Optional type filter
            limit: Maximum results to return

        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        results = []

        for entry_meta in self.store.list_entries(entry_type):
            # Check title match
            if query_lower in entry_meta["title"].lower():
                entry = self.store.get_entry(entry_meta["id"])
                if entry:
                    results.append(entry)
                continue

            # Check tag match
            for tag in entry_meta.get("tags", []):
                if query_lower in tag.lower():
                    entry = self.store.get_entry(entry_meta["id"])
                    if entry:
                        results.append(entry)
                    break

            if len(results) >= limit:
                break

        return results[:limit]

    def get_recent(
        self,
        limit: int = 10,
        entry_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get most recent entries.

        Args:
            limit: Maximum results
            entry_type: Optional type filter

        Returns:
            List of recent entries
        """
        entries = self.store.list_entries(entry_type)

        # Sort by created_at descending
        entries.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        results = []
        for entry_meta in entries[:limit]:
            entry = self.store.get_entry(entry_meta["id"])
            if entry:
                results.append(entry)

        return results

    def get_by_tags(
        self,
        tags: List[str],
        match_all: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get entries by multiple tags.

        Args:
            tags: List of tags to search
            match_all: If True, entry must have all tags

        Returns:
            List of matching entries
        """
        if match_all:
            # Find entries with all tags
            result_sets = [set(self.store._index["tags"].get(tag, [])) for tag in tags]
            if not result_sets:
                return []
            common_ids = result_sets[0].intersection(*result_sets[1:])
            return [self.store.get_entry(eid) for eid in common_ids if self.store.get_entry(eid)]
        else:
            # Find entries with any tag
            all_ids = set()
            for tag in tags:
                all_ids.update(self.store._index["tags"].get(tag, []))
            return [self.store.get_entry(eid) for eid in all_ids if self.store.get_entry(eid)]
