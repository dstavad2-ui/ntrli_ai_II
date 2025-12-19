# ============================================================================
# NTRLI' AI - KNOWLEDGE CACHE (OFFLINE RESILIENCE)
# ============================================================================
"""
Local knowledge cache for offline resilience.

Stores research results and other data for later retrieval,
enabling the system to work with previously gathered information
when external sources are unavailable.
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


# Default cache root directory
CACHE_ROOT = Path("knowledge_cache")


def _ensure_cache_dir() -> Path:
    """Ensure the cache directory exists."""
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    return CACHE_ROOT


def _hash_key(topic: str) -> str:
    """Generate a hash key for a topic."""
    return hashlib.sha256(topic.encode()).hexdigest()


def store(topic: str, data: Any) -> str:
    """
    Store data in the knowledge cache.

    Args:
        topic: The topic/key for this data
        data: The data to store (must be JSON-serializable)

    Returns:
        The cache key (hash)
    """
    _ensure_cache_dir()
    key = _hash_key(topic)
    cache_file = CACHE_ROOT / f"{key}.json"

    cache_entry = {
        "topic": topic,
        "data": data,
        "stored_at": datetime.utcnow().isoformat(),
        "version": 1
    }

    cache_file.write_text(json.dumps(cache_entry, indent=2))
    return key


def load(topic: str) -> Optional[Any]:
    """
    Load data from the knowledge cache.

    Args:
        topic: The topic/key to look up

    Returns:
        The cached data, or None if not found
    """
    _ensure_cache_dir()
    key = _hash_key(topic)
    cache_file = CACHE_ROOT / f"{key}.json"

    if not cache_file.exists():
        return None

    try:
        cached = json.loads(cache_file.read_text())
        return cached.get("data")
    except (json.JSONDecodeError, KeyError):
        return None


def load_with_metadata(topic: str) -> Optional[Dict[str, Any]]:
    """
    Load data with metadata from the knowledge cache.

    Args:
        topic: The topic/key to look up

    Returns:
        Dict with 'data', 'stored_at', 'topic', or None if not found
    """
    _ensure_cache_dir()
    key = _hash_key(topic)
    cache_file = CACHE_ROOT / f"{key}.json"

    if not cache_file.exists():
        return None

    try:
        return json.loads(cache_file.read_text())
    except json.JSONDecodeError:
        return None


def exists(topic: str) -> bool:
    """Check if a topic exists in the cache."""
    key = _hash_key(topic)
    return (CACHE_ROOT / f"{key}.json").exists()


def delete(topic: str) -> bool:
    """
    Delete a topic from the cache.

    Args:
        topic: The topic to delete

    Returns:
        True if deleted, False if not found
    """
    key = _hash_key(topic)
    cache_file = CACHE_ROOT / f"{key}.json"

    if cache_file.exists():
        cache_file.unlink()
        return True
    return False


def clear_cache() -> int:
    """
    Clear all cached data.

    Returns:
        Number of entries deleted
    """
    _ensure_cache_dir()
    count = 0
    for cache_file in CACHE_ROOT.glob("*.json"):
        cache_file.unlink()
        count += 1
    return count


def list_topics() -> List[str]:
    """
    List all cached topics.

    Returns:
        List of topic strings
    """
    _ensure_cache_dir()
    topics = []
    for cache_file in CACHE_ROOT.glob("*.json"):
        try:
            cached = json.loads(cache_file.read_text())
            topics.append(cached.get("topic", "unknown"))
        except (json.JSONDecodeError, KeyError):
            continue
    return topics


def get_cache_stats() -> Dict[str, Any]:
    """Get statistics about the cache."""
    _ensure_cache_dir()
    files = list(CACHE_ROOT.glob("*.json"))
    total_size = sum(f.stat().st_size for f in files)

    return {
        "entries": len(files),
        "total_size_bytes": total_size,
        "cache_dir": str(CACHE_ROOT.absolute())
    }
