# ============================================================================
# NTRLI' AI - ORCHESTRATOR (EXECUTION CORE)
# ============================================================================
"""
The orchestrator is the execution core of NTRLI' AI.

It coordinates:
1. Planning - decomposing tasks into steps
2. Execution - running steps via the executor
3. Recovery - retrying on failure

BEHAVIORAL LAWS enforced:
- No output without a plan
- No execution without verification
- No silent failure
"""

from typing import Dict, Any
from planner import Planner
from step_executor import StepExecutor
from failure_recovery import FailureRecovery
from providers.router import Router


class Orchestrator:
    """
    Execution core coordinating plan -> execute -> recover.
    """

    def __init__(self, router: Router):
        """
        Initialize orchestrator with LLM router.

        Args:
            router: The LLM router for plan generation
        """
        self.planner = Planner(router)
        self.executor = StepExecutor()
        self.recovery = FailureRecovery()
        self.router = router

    def execute(
        self,
        conversation_id: str,
        instruction: str
    ) -> Dict[str, Any]:
        """
        Execute an instruction with planning and retry logic.

        Args:
            conversation_id: Unique identifier for this execution
            instruction: The task instruction

        Returns:
            Execution context with all results

        Raises:
            RecoveryError: If execution fails after all retries
        """
        def execution_attempt() -> Dict[str, Any]:
            # Step 1: Generate plan (BEHAVIORAL LAW: No output without a plan)
            steps = self.planner.plan(instruction)

            # Step 2: Execute plan
            return self.executor.execute(conversation_id, steps)

        # Execute with retry logic
        return self.recovery.retry(
            execution_attempt,
            description=f"instruction execution: {instruction[:50]}..."
        )

    def execute_with_plan(
        self,
        conversation_id: str,
        instruction: str
    ) -> tuple[list, Dict[str, Any]]:
        """
        Execute and return both plan and results.

        Useful for debugging and transparency.

        Args:
            conversation_id: Unique identifier for this execution
            instruction: The task instruction

        Returns:
            Tuple of (plan steps, execution context)
        """
        steps = self.planner.plan(instruction)
        context = self.executor.execute(conversation_id, steps)
        return steps, context
