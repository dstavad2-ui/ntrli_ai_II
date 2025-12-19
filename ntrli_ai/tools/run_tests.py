# ============================================================================
# NTRLI' AI - TEST EXECUTION TOOL
# ============================================================================
"""
Test execution tool using pytest.

BEHAVIORAL LAW: No writing to GitHub without tests.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any
from .registry import register_tool


class RunTests:
    """Execute pytest on provided test files."""

    name = "run_tests"

    def run(self, payload: dict) -> dict:
        """
        Run pytest on provided test files.

        Args:
            payload: Must contain "files" dict with test files

        Returns:
            Dictionary with test results
        """
        files = payload.get("files", {})
        timeout = payload.get("timeout", 60)

        if not files:
            return {
                "passed": False,
                "error": "No files provided",
                "output": "",
                "errors": "",
                "returncode": -1
            }

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)

                # Write all files
                for filename, code in files.items():
                    filepath = root / filename
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                    filepath.write_text(code)

                # Run pytest
                result = subprocess.run(
                    ["python", "-m", "pytest", "-v", str(root)],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(root)
                )

                return {
                    "passed": result.returncode == 0,
                    "output": result.stdout,
                    "errors": result.stderr,
                    "returncode": result.returncode
                }

        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "error": f"Tests timed out after {timeout}s",
                "output": "",
                "errors": "",
                "returncode": -1
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "output": "",
                "errors": "",
                "returncode": -1
            }


# Register the tool
register_tool(RunTests())
