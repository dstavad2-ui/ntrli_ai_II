# ============================================================================
# NTRLI' AI - WEB RESEARCH TOOL
# ============================================================================
"""
Web research tool for gathering external information.

Uses DuckDuckGo HTML search for privacy-respecting web queries.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
from .registry import register_tool


class WebResearch:
    """Web research tool using DuckDuckGo."""

    name = "research"

    def run(self, payload: dict) -> dict:
        """
        Execute web research query.

        Args:
            payload: Must contain "query" key

        Returns:
            Dictionary with search results
        """
        query = payload.get("query", "")
        if not query:
            return {"error": "No query provided", "results": []}

        try:
            # DuckDuckGo HTML search
            response = requests.post(
                "https://html.duckduckgo.com/html/",
                data={"q": query},
                headers={"User-Agent": "Mozilla/5.0 (compatible; NTRLI-AI/1.0)"},
                timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results: List[Dict[str, str]] = []

            for result in soup.select(".result")[:5]:
                link = result.select_one(".result__a")
                snippet = result.select_one(".result__snippet")

                if link:
                    results.append({
                        "title": link.get_text(strip=True),
                        "url": link.get("href", ""),
                        "snippet": snippet.get_text(strip=True) if snippet else ""
                    })

            return {"results": results, "query": query, "count": len(results)}

        except requests.RequestException as e:
            return {"error": str(e), "results": [], "query": query}


# Register the tool
register_tool(WebResearch())
