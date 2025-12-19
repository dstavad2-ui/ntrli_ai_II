# ============================================================================
# NTRLI' AI - CONTROL PLANE (SINGLE COMMAND GATE)
# ============================================================================
"""
The control plane is the ONLY entry point for NTRLI' AI.

BEHAVIORAL LAW: Only EXECUTE command is allowed.

This gate ensures:
1. Only valid commands pass through
2. All execution is traceable
3. No unauthorized operations
"""

from typing import Dict, Any
from orchestrator import Orchestrator
from providers.router import Router


class CommandError(RuntimeError):
    """Raised when an invalid command is received."""
    pass


class ControlPlane:
    """
    Single command gate - the only entry point.

    BEHAVIORAL LAW: Only EXECUTE command is allowed.
    """

    ALLOWED_COMMAND = "EXECUTE"

    def __init__(self, router: Router):
        """
        Initialize control plane with LLM router.

        Args:
            router: The LLM router for the orchestrator
        """
        self.orchestrator = Orchestrator(router)

    def handle(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming command.

        Only EXECUTE command is allowed. All other commands are rejected.

        Args:
            payload: Must contain:
                - command: Must be "EXECUTE"
                - conversation_id: Unique identifier
                - instructions: The task to execute

        Returns:
            Execution results from the orchestrator

        Raises:
            CommandError: If command is not EXECUTE
        """
        command = payload.get("command")

        if command != self.ALLOWED_COMMAND:
            raise CommandError(
                f"Only {self.ALLOWED_COMMAND} command allowed, got: {command}"
            )

        conversation_id = payload.get("conversation_id", "default")
        instructions = payload.get("instructions", "")

        if not instructions:
            raise CommandError("No instructions provided")

        return self.orchestrator.execute(conversation_id, instructions)

    def handle_with_trace(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle command with full trace output.

        Returns both the plan and execution results for transparency.

        Args:
            payload: Same as handle()

        Returns:
            Dict with 'plan' and 'results' keys
        """
        command = payload.get("command")

        if command != self.ALLOWED_COMMAND:
            raise CommandError(
                f"Only {self.ALLOWED_COMMAND} command allowed, got: {command}"
            )

        conversation_id = payload.get("conversation_id", "default")
        instructions = payload.get("instructions", "")

        if not instructions:
            raise CommandError("No instructions provided")

        plan, results = self.orchestrator.execute_with_plan(
            conversation_id,
            instructions
        )

        return {
            "plan": plan,
            "results": results
        }
