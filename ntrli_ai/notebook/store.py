# ============================================================================
# NTRLI' AI - NOTEBOOK STORE
# ============================================================================
"""
Notebook store for persistent knowledge storage.

Provides structured storage for research results, code snippets,
and other artifacts that need to persist across sessions.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class NotebookStore:
    """
    Persistent notebook storage.

    Stores entries with metadata for later retrieval.
    """

    def __init__(self, store_dir: str = "notebook_data"):
        """
        Initialize notebook store.

        Args:
            store_dir: Directory for storing notebook data
        """
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self._index_file = self.store_dir / "index.json"
        self._index = self._load_index()

    def _load_index(self) -> Dict[str, Any]:
        """Load or create the index."""
        if self._index_file.exists():
            return json.loads(self._index_file.read_text())
        return {"entries": {}, "tags": {}}

    def _save_index(self) -> None:
        """Save the index to disk."""
        self._index_file.write_text(json.dumps(self._index, indent=2))

    def add_entry(
        self,
        title: str,
        content: Any,
        tags: Optional[List[str]] = None,
        entry_type: str = "note"
    ) -> str:
        """
        Add an entry to the notebook.

        Args:
            title: Entry title
            content: Entry content (must be JSON-serializable)
            tags: Optional list of tags
            entry_type: Type of entry (note, code, research, etc.)

        Returns:
            Entry ID
        """
        entry_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{len(self._index['entries'])}"

        entry = {
            "id": entry_id,
            "title": title,
            "content": content,
            "type": entry_type,
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        # Save entry file
        entry_file = self.store_dir / f"{entry_id}.json"
        entry_file.write_text(json.dumps(entry, indent=2))

        # Update index
        self._index["entries"][entry_id] = {
            "title": title,
            "type": entry_type,
            "tags": tags or [],
            "created_at": entry["created_at"]
        }

        # Update tag index
        for tag in (tags or []):
            if tag not in self._index["tags"]:
                self._index["tags"][tag] = []
            self._index["tags"][tag].append(entry_id)

        self._save_index()
        return entry_id

    def get_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an entry by ID.

        Args:
            entry_id: The entry ID

        Returns:
            Entry dict or None if not found
        """
        entry_file = self.store_dir / f"{entry_id}.json"
        if entry_file.exists():
            return json.loads(entry_file.read_text())
        return None

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Search entries by tag.

        Args:
            tag: Tag to search for

        Returns:
            List of matching entries
        """
        entry_ids = self._index["tags"].get(tag, [])
        return [self.get_entry(eid) for eid in entry_ids if self.get_entry(eid)]

    def list_entries(self, entry_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all entries, optionally filtered by type.

        Args:
            entry_type: Optional type filter

        Returns:
            List of entry summaries
        """
        entries = []
        for entry_id, meta in self._index["entries"].items():
            if entry_type is None or meta["type"] == entry_type:
                entries.append({"id": entry_id, **meta})
        return entries
