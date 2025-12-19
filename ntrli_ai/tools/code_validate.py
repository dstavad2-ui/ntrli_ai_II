# ============================================================================
# NTRLI' AI - CODE VALIDATION TOOL
# ============================================================================
"""
Code validation tool using Python AST.

BEHAVIORAL LAW: No code without validation.
"""

import ast
from typing import Dict, List, Any
from .registry import register_tool


class CodeValidate:
    """Python code syntax validation using AST."""

    name = "code_validate"

    def run(self, payload: dict) -> dict:
        """
        Validate Python code syntax.

        Args:
            payload: Must contain "files" dict mapping filenames to code

        Returns:
            Dictionary with validation results
        """
        files = payload.get("files", {})
        if not files:
            return {"valid": False, "errors": [{"error": "No files provided"}]}

        errors: List[Dict[str, Any]] = []
        validated_files: List[str] = []

        for filename, code in files.items():
            try:
                ast.parse(code)
                validated_files.append(filename)
            except SyntaxError as e:
                errors.append({
                    "file": filename,
                    "line": e.lineno,
                    "offset": e.offset,
                    "error": str(e.msg) if e.msg else str(e)
                })

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "validated_files": validated_files,
            "total_files": len(files)
        }


# Register the tool
register_tool(CodeValidate())
