# ============================================================================
# NTRLI' AI - NOTEBOOK MODULE
# ============================================================================
"""
Notebook module for knowledge storage and retrieval.
"""

from .store import NotebookStore
from .query import NotebookQueryEngine

__all__ = ["NotebookStore", "NotebookQueryEngine"]
