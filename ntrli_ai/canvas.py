# ============================================================================
# NTRLI' AI - CANVAS (EXECUTION CONTEXT)
# ============================================================================
"""
Canvas module for maintaining execution context.

The canvas holds all state for a single execution session,
including intermediate results, artifacts, and execution trace.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class CanvasEntry:
    """A single entry in the canvas."""
    key: str
    value: Any
    entry_type: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class Canvas:
    """
    Execution context canvas.

    Holds all state for a single execution session.
    """

    def __init__(self, conversation_id: str):
        """
        Initialize canvas.

        Args:
            conversation_id: Unique identifier for this session
        """
        self.conversation_id = conversation_id
        self.created_at = datetime.utcnow().isoformat()
        self._entries: Dict[str, CanvasEntry] = {}
        self._trace: List[Dict[str, Any]] = []

    def set(
        self,
        key: str,
        value: Any,
        entry_type: str = "data",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Set a value in the canvas.

        Args:
            key: Entry key
            value: Entry value
            entry_type: Type of entry (data, artifact, result, etc.)
            metadata: Optional metadata
        """
        entry = CanvasEntry(
            key=key,
            value=value,
            entry_type=entry_type,
            metadata=metadata or {}
        )
        self._entries[key] = entry

        # Add to trace
        self._trace.append({
            "action": "set",
            "key": key,
            "type": entry_type,
            "timestamp": entry.timestamp
        })

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the canvas.

        Args:
            key: Entry key
            default: Default value if not found

        Returns:
            Entry value or default
        """
        entry = self._entries.get(key)
        return entry.value if entry else default

    def has(self, key: str) -> bool:
        """Check if key exists in canvas."""
        return key in self._entries

    def get_entry(self, key: str) -> Optional[CanvasEntry]:
        """Get full entry including metadata."""
        return self._entries.get(key)

    def list_keys(self, entry_type: Optional[str] = None) -> List[str]:
        """
        List all keys, optionally filtered by type.

        Args:
            entry_type: Optional type filter

        Returns:
            List of keys
        """
        if entry_type:
            return [k for k, v in self._entries.items() if v.entry_type == entry_type]
        return list(self._entries.keys())

    def get_trace(self) -> List[Dict[str, Any]]:
        """Get execution trace."""
        return self._trace.copy()

    def to_dict(self) -> Dict[str, Any]:
        """
        Export canvas as dictionary.

        Returns:
            Dict with all canvas data
        """
        return {
            "conversation_id": self.conversation_id,
            "created_at": self.created_at,
            "entries": {
                k: {
                    "value": v.value,
                    "type": v.entry_type,
                    "timestamp": v.timestamp,
                    "metadata": v.metadata
                }
                for k, v in self._entries.items()
            },
            "trace": self._trace
        }

    def clear(self) -> None:
        """Clear all entries (trace is preserved)."""
        self._entries.clear()
        self._trace.append({
            "action": "clear",
            "timestamp": datetime.utcnow().isoformat()
        })
