# ============================================================================
# NTRLI' AI - STEP EXECUTOR (NO IMPLICIT BEHAVIOR)
# ============================================================================
"""
The step executor runs planned steps sequentially.

BEHAVIORAL LAWS:
- No execution without verification
- No implicit behavior
- No silent failure

Each step must:
1. Have a verified capability
2. Use a registered tool
3. Return a structured result
"""

from typing import List, Dict, Any
from tools.registry import get as get_tool
from capabilities import assert_capability


class ExecutionError(RuntimeError):
    """Raised when step execution fails - no silent failure."""
    pass


class StepExecutor:
    """
    Sequential step executor with no implicit behavior.

    All behavior is explicit and traceable.
    """

    def execute(
        self,
        conversation_id: str,
        steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Execute steps sequentially, building context.

        Each step's result is stored in context for subsequent steps.

        Args:
            conversation_id: Unique identifier for this execution
            steps: List of steps from the planner

        Returns:
            Execution context with all step results

        Raises:
            ExecutionError: If any step fails
        """
        context: Dict[str, Any] = {
            "conversation_id": conversation_id,
            "steps_executed": 0,
            "steps_total": len(steps)
        }

        for i, step in enumerate(steps):
            action = step["action"]
            payload = step.get("payload", {})

            # BEHAVIORAL LAW: No execution without verified capabilities
            try:
                assert_capability(action)
            except Exception as e:
                raise ExecutionError(f"Step {i} ({action}): capability check failed - {e}")

            # Get the registered tool
            try:
                tool = get_tool(action)
            except KeyError as e:
                raise ExecutionError(f"Step {i} ({action}): tool not found - {e}")

            # Execute the step
            try:
                result = tool.run({
                    **payload,
                    "conversation_id": conversation_id,
                    "context": context
                })

                # Store result in context
                context[action] = result
                context[f"step_{i}"] = {
                    "action": action,
                    "payload": payload,
                    "result": result
                }
                context["steps_executed"] = i + 1

            except Exception as e:
                # BEHAVIORAL LAW: No silent failure
                raise ExecutionError(f"Step {i} ({action}) failed: {e}")

        return context
