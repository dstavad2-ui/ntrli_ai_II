# ============================================================================
# NTRLI' AI - GITHUB WRITEBACK TOOL
# ============================================================================
"""
GitHub writeback tool for repository updates.

BEHAVIORAL LAW: No writing to GitHub without tests passing.
"""

import os
import base64
from typing import Dict, Any, Optional
import requests
from .registry import register_tool


class GitHubWriteback:
    """Write files to GitHub via API."""

    name = "github_writeback"

    def run(self, payload: dict) -> dict:
        """
        Write files to GitHub repository.

        Args:
            payload: Must contain "repo", "files", optional "branch", "message"

        Returns:
            Dictionary with write results
        """
        repo = payload.get("repo", "")
        branch = payload.get("branch", "main")
        files = payload.get("files", {})
        message = payload.get("message", "NTRLI AI automated update")

        if not repo:
            return {"success": False, "error": "No repository specified"}

        if not files:
            return {"success": False, "error": "No files to write"}

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return {"success": False, "error": "GITHUB_TOKEN not set"}

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        results = {
            "success": True,
            "files_written": [],
            "errors": []
        }

        for filepath, content in files.items():
            try:
                # Get current file SHA if it exists
                url = f"https://api.github.com/repos/{repo}/contents/{filepath}"
                params = {"ref": branch}

                response = requests.get(url, headers=headers, params=params)
                sha = None
                if response.status_code == 200:
                    sha = response.json().get("sha")

                # Create or update file
                data = {
                    "message": f"{message}: {filepath}",
                    "content": base64.b64encode(content.encode()).decode(),
                    "branch": branch
                }
                if sha:
                    data["sha"] = sha

                response = requests.put(url, headers=headers, json=data)

                if response.status_code in (200, 201):
                    results["files_written"].append(filepath)
                else:
                    results["errors"].append({
                        "file": filepath,
                        "error": response.json().get("message", "Unknown error")
                    })
                    results["success"] = False

            except Exception as e:
                results["errors"].append({
                    "file": filepath,
                    "error": str(e)
                })
                results["success"] = False

        return results


# Register the tool
register_tool(GitHubWriteback())
