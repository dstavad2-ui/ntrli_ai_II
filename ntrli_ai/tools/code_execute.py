# ============================================================================
# NTRLI' AI - CODE EXECUTION TOOL
# ============================================================================
"""
Code execution tool with sandbox isolation.

Executes Python code in isolated temporary directories.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any
from .registry import register_tool


class CodeExecute:
    """Execute Python code in isolated sandbox."""

    name = "code_execute"

    def run(self, payload: dict) -> dict:
        """
        Execute Python code in isolated temp directory.

        Args:
            payload: Must contain "files" dict and optional "entry" point

        Returns:
            Dictionary with execution results
        """
        files = payload.get("files", {})
        entry = payload.get("entry", "main.py")
        timeout = payload.get("timeout", 30)

        if not files:
            return {
                "success": False,
                "error": "No files provided",
                "stdout": "",
                "stderr": "",
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

                # Execute entry point
                result = subprocess.run(
                    ["python", str(root / entry)],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(root)
                )

                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout}s",
                "stdout": "",
                "stderr": "",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "returncode": -1
            }


# Register the tool
register_tool(CodeExecute())
