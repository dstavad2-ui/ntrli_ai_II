# ============================================================================
# NTRLI' AI - ARTIFACT WRITE TOOL
# ============================================================================
"""
Artifact writing tool for persisting outputs.

Writes generated artifacts to the local filesystem.
"""

from pathlib import Path
from typing import Dict, Any
from .registry import register_tool


class ArtifactWrite:
    """Write artifacts to filesystem."""

    name = "artifact_write"

    def __init__(self, output_dir: str = "artifacts"):
        self.output_dir = Path(output_dir)

    def run(self, payload: dict) -> dict:
        """
        Write artifacts to filesystem.

        Args:
            payload: Must contain "files" dict mapping filenames to content

        Returns:
            Dictionary with write results
        """
        files = payload.get("files", {})
        output_dir = payload.get("output_dir", str(self.output_dir))

        if not files:
            return {"success": False, "error": "No files provided", "written": []}

        output_path = Path(output_dir)

        try:
            output_path.mkdir(parents=True, exist_ok=True)

            written = []
            for filename, content in files.items():
                filepath = output_path / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_text(content)
                written.append(str(filepath))

            return {
                "success": True,
                "written": written,
                "output_dir": str(output_path)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "written": []
            }


# Register the tool
register_tool(ArtifactWrite())
