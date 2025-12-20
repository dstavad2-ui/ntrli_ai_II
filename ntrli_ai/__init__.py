# ============================================================================
# NTRLI' AI - Deterministic, Execution-First Artificial Intelligence System
# ============================================================================
"""
NTRLI' AI

A command-driven execution engine that performs real work—planning, research,
coding, validation, and GitHub administration—under strict mechanical constraints.

ABSOLUTE BEHAVIORAL LAWS (Non-Negotiable):
1. No output without a plan
2. No plan without validation
3. No code without intent
4. No execution without verification
5. No writing to GitHub without tests
6. No hallucination
7. No filler
8. No goal drift
9. No silent failure
10. No autonomy

CORE SEGREGATION RULE:
AI and commercial operations are strictly segregated.
AI cannot make decisions in transactional/commercial flows.

If any law is violated, execution halts.
"""

__version__ = "1.0.0"
__author__ = "NTRLI AI"

from .capabilities import (
    assert_capability,
    list_capabilities,
    CAPABILITIES,
)

from .control_plane import ControlPlane
from .orchestrator import Orchestrator
from .planner import Planner
from .step_executor import StepExecutor
from .failure_recovery import FailureRecovery

from .segregation import (
    SegregationEnforcer,
    OperationType,
    TelegramShopBoundary,
    SegregationViolation,
)

__all__ = [
    "ControlPlane",
    "Orchestrator",
    "Planner",
    "StepExecutor",
    "FailureRecovery",
    "assert_capability",
    "list_capabilities",
    "CAPABILITIES",
    "SegregationEnforcer",
    "OperationType",
    "TelegramShopBoundary",
    "SegregationViolation",
]
