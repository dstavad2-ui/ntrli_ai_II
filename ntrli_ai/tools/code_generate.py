# ============================================================================
# NTRLI' AI - CODE GENERATION TOOL
# ============================================================================
"""
Code generation tool.

Generates code based on specifications using LLM providers.
This tool requires a router to be injected at runtime.
"""

from typing import Dict, Any, Optional
from .registry import register_tool


class CodeGenerate:
    """Generate code based on specifications."""

    name = "code_generate"

    def __init__(self):
        self._router = None

    def set_router(self, router) -> None:
        """Inject the LLM router for code generation."""
        self._router = router

    def run(self, payload: dict) -> dict:
        """
        Generate code based on specification.

        Args:
            payload: Must contain "spec" with code specification

        Returns:
            Dictionary with generated code files
        """
        spec = payload.get("spec", "")
        language = payload.get("language", "python")
        context = payload.get("context", {})

        if not spec:
            return {"error": "No specification provided", "files": {}}

        if not self._router:
            return {"error": "Router not configured", "files": {}}

        # Build prompt for code generation
        prompt = f"""Generate {language} code based on this specification.
Return ONLY the code, no explanations.

SPECIFICATION:
{spec}

CONTEXT:
{context}

Return the code in a format where each file is clearly marked:
# FILE: filename.py
<code>

# FILE: another_file.py
<code>
"""

        try:
            outputs = self._router.generate(prompt, temperature=0.0)

            # Parse the first successful output
            for provider_name, output in outputs.items():
                if not output.startswith("ERROR:"):
                    files = self._parse_files(output)
                    return {
                        "files": files,
                        "provider": provider_name,
                        "spec": spec
                    }

            return {"error": "All providers failed", "files": {}}

        except Exception as e:
            return {"error": str(e), "files": {}}

    def _parse_files(self, output: str) -> Dict[str, str]:
        """Parse generated output into file dictionary."""
        files = {}
        current_file = None
        current_content = []

        for line in output.split("\n"):
            if line.startswith("# FILE:"):
                # Save previous file
                if current_file:
                    files[current_file] = "\n".join(current_content)

                # Start new file
                current_file = line.replace("# FILE:", "").strip()
                current_content = []
            elif current_file:
                current_content.append(line)

        # Save last file
        if current_file:
            files[current_file] = "\n".join(current_content)

        # If no files parsed, treat entire output as main.py
        if not files:
            files["main.py"] = output

        return files


# Register the tool
register_tool(CodeGenerate())
