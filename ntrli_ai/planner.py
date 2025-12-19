# ============================================================================
# NTRLI' AI - PLANNER (PLAN-FIRST ENFORCEMENT)
# ============================================================================
"""
The planner enforces the first behavioral law: No output without a plan.

All execution must go through the planner, which:
1. Decomposes tasks into ordered steps
2. Validates the plan against a JSON schema
3. Returns only valid, executable plans

If planning fails, execution MUST halt.
"""

import json
from typing import List, Dict, Any
from jsonschema import validate, ValidationError
from providers.router import Router


# JSON Schema for plan validation
PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "research", "notebook_query", "code_generate",
                            "code_validate", "run_tests", "code_execute",
                            "artifact_write", "github_writeback"
                        ]
                    },
                    "payload": {"type": "object"}
                },
                "required": ["action"]
            },
            "minItems": 1
        }
    },
    "required": ["steps"]
}


class PlanningError(RuntimeError):
    """Raised when planning fails - execution MUST halt."""
    pass


class Planner:
    """
    Plan-first enforcement engine.

    BEHAVIORAL LAW: No output without a plan.
    """

    def __init__(self, router: Router):
        """
        Initialize planner with LLM router.

        Args:
            router: The LLM router for plan generation
        """
        self.router = router

    def plan(self, instruction: str) -> List[Dict[str, Any]]:
        """
        Generate a validated execution plan.

        MUST return valid JSON matching PLAN_SCHEMA.
        If planning fails, raises PlanningError.

        Args:
            instruction: The task instruction

        Returns:
            List of execution steps

        Raises:
            PlanningError: If planning fails
        """
        prompt = f"""You are a deterministic planning engine.
Return ONLY valid JSON. No commentary. No markdown. No explanations.

Decompose this task into ordered steps.

ALLOWED ACTIONS:
- research: Web research for gathering information
- notebook_query: Query the knowledge cache
- code_generate: Generate code files based on specification
- code_validate: Validate Python code syntax
- run_tests: Execute test suite
- code_execute: Run code in isolated sandbox
- artifact_write: Write output files to disk
- github_writeback: Write files to GitHub repository

TASK:
{instruction}

REQUIRED FORMAT (JSON only, no other text):
{{"steps": [{{"action": "research", "payload": {{"query": "..."}}}}, {{"action": "code_generate", "payload": {{"spec": "..."}}}}]}}
"""

        outputs = self.router.generate(prompt, temperature=0.0)

        # Try each provider's output
        for provider_name, text in outputs.items():
            if text.startswith("ERROR:"):
                continue

            try:
                # Extract JSON from potential markdown code blocks
                parsed_text = self._extract_json(text)
                data = json.loads(parsed_text)
                validate(instance=data, schema=PLAN_SCHEMA)
                return data["steps"]

            except (json.JSONDecodeError, ValidationError):
                continue

        raise PlanningError("All providers failed to generate valid plan")

    def _extract_json(self, text: str) -> str:
        """Extract JSON from potential markdown code blocks."""
        text = text.strip()

        # Remove markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1].strip()

        # Try to find JSON object boundaries
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]

        return text
