# ============================================================================
# NTRLI' AI - GITHUB WRITE CLIENT
# ============================================================================
"""
GitHub API client for repository write operations.

BEHAVIORAL LAW: No writing to GitHub without tests passing.
"""

import os
import base64
from typing import Dict, List, Optional, Any
import requests


class GitHubWriteClient:
    """
    GitHub API client for write operations.

    Provides methods for creating/updating files, branches, and pull requests.
    """

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client.

        Args:
            token: GitHub API token (defaults to GITHUB_TOKEN env var)
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required (set GITHUB_TOKEN or pass token)")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"

    def get_file(
        self,
        repo: str,
        path: str,
        branch: str = "main"
    ) -> Optional[Dict[str, Any]]:
        """
        Get file content and metadata.

        Args:
            repo: Repository in 'owner/repo' format
            path: File path in repository
            branch: Branch name

        Returns:
            File metadata including sha and content, or None if not found
        """
        url = f"{self.base_url}/repos/{repo}/contents/{path}"
        response = requests.get(
            url,
            headers=self.headers,
            params={"ref": branch}
        )

        if response.status_code == 200:
            return response.json()
        return None

    def create_or_update_file(
        self,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Create or update a file in the repository.

        Args:
            repo: Repository in 'owner/repo' format
            path: File path in repository
            content: File content
            message: Commit message
            branch: Branch name

        Returns:
            API response with commit details
        """
        url = f"{self.base_url}/repos/{repo}/contents/{path}"

        # Check if file exists to get SHA
        existing = self.get_file(repo, path, branch)
        sha = existing.get("sha") if existing else None

        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }
        if sha:
            data["sha"] = sha

        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def write_files(
        self,
        repo: str,
        files: Dict[str, str],
        message: str,
        branch: str = "main"
    ) -> List[Dict[str, Any]]:
        """
        Write multiple files to repository.

        Args:
            repo: Repository in 'owner/repo' format
            files: Dict mapping paths to content
            message: Commit message prefix
            branch: Branch name

        Returns:
            List of API responses for each file
        """
        results = []
        for path, content in files.items():
            result = self.create_or_update_file(
                repo=repo,
                path=path,
                content=content,
                message=f"{message}: {path}",
                branch=branch
            )
            results.append(result)
        return results

    def create_branch(
        self,
        repo: str,
        branch_name: str,
        from_branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Create a new branch.

        Args:
            repo: Repository in 'owner/repo' format
            branch_name: Name for new branch
            from_branch: Branch to create from

        Returns:
            API response
        """
        # Get SHA of source branch
        ref_url = f"{self.base_url}/repos/{repo}/git/ref/heads/{from_branch}"
        response = requests.get(ref_url, headers=self.headers)
        response.raise_for_status()
        sha = response.json()["object"]["sha"]

        # Create new branch
        create_url = f"{self.base_url}/repos/{repo}/git/refs"
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
        response = requests.post(create_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_pull_request(
        self,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> Dict[str, Any]:
        """
        Create a pull request.

        Args:
            repo: Repository in 'owner/repo' format
            title: PR title
            body: PR description
            head: Source branch
            base: Target branch

        Returns:
            API response with PR details
        """
        url = f"{self.base_url}/repos/{repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
