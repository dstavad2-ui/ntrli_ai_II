# ============================================================================
# NTRLI' AI - SELF METRICS
# ============================================================================
"""
Self-monitoring and metrics collection.

Tracks execution performance, success rates, and system health.
This is how NTRLI' AI maintains awareness of its own performance.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class ExecutionMetric:
    """Metrics for a single execution."""
    conversation_id: str
    instruction: str
    started_at: str
    completed_at: Optional[str] = None
    success: bool = False
    steps_planned: int = 0
    steps_executed: int = 0
    error: Optional[str] = None
    duration_seconds: Optional[float] = None
    provider_used: Optional[str] = None


class SelfMetrics:
    """
    Self-monitoring system for NTRLI' AI.

    Collects and reports on execution metrics.
    """

    def __init__(self, metrics_dir: str = "metrics"):
        """
        Initialize metrics collector.

        Args:
            metrics_dir: Directory for storing metrics
        """
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self._current_metrics: Dict[str, ExecutionMetric] = {}
        self._history: List[ExecutionMetric] = []

    def start_execution(
        self,
        conversation_id: str,
        instruction: str
    ) -> None:
        """
        Record start of execution.

        Args:
            conversation_id: Execution identifier
            instruction: The instruction being executed
        """
        self._current_metrics[conversation_id] = ExecutionMetric(
            conversation_id=conversation_id,
            instruction=instruction[:200],  # Truncate long instructions
            started_at=datetime.utcnow().isoformat()
        )

    def record_plan(
        self,
        conversation_id: str,
        steps_count: int
    ) -> None:
        """
        Record plan generation.

        Args:
            conversation_id: Execution identifier
            steps_count: Number of steps in plan
        """
        if conversation_id in self._current_metrics:
            self._current_metrics[conversation_id].steps_planned = steps_count

    def record_step(
        self,
        conversation_id: str,
        step_number: int
    ) -> None:
        """
        Record step completion.

        Args:
            conversation_id: Execution identifier
            step_number: Completed step number (0-indexed)
        """
        if conversation_id in self._current_metrics:
            self._current_metrics[conversation_id].steps_executed = step_number + 1

    def complete_execution(
        self,
        conversation_id: str,
        success: bool,
        error: Optional[str] = None,
        provider: Optional[str] = None
    ) -> ExecutionMetric:
        """
        Record execution completion.

        Args:
            conversation_id: Execution identifier
            success: Whether execution succeeded
            error: Error message if failed
            provider: Provider that was used

        Returns:
            The completed metric
        """
        if conversation_id not in self._current_metrics:
            raise ValueError(f"No execution started for {conversation_id}")

        metric = self._current_metrics[conversation_id]
        metric.completed_at = datetime.utcnow().isoformat()
        metric.success = success
        metric.error = error
        metric.provider_used = provider

        # Calculate duration
        start = datetime.fromisoformat(metric.started_at)
        end = datetime.fromisoformat(metric.completed_at)
        metric.duration_seconds = (end - start).total_seconds()

        # Move to history
        self._history.append(metric)
        del self._current_metrics[conversation_id]

        # Persist
        self._save_metric(metric)

        return metric

    def _save_metric(self, metric: ExecutionMetric) -> None:
        """Save metric to disk."""
        date_str = datetime.utcnow().strftime("%Y%m%d")
        metrics_file = self.metrics_dir / f"metrics_{date_str}.jsonl"

        with open(metrics_file, "a") as f:
            f.write(json.dumps({
                "conversation_id": metric.conversation_id,
                "instruction": metric.instruction,
                "started_at": metric.started_at,
                "completed_at": metric.completed_at,
                "success": metric.success,
                "steps_planned": metric.steps_planned,
                "steps_executed": metric.steps_executed,
                "error": metric.error,
                "duration_seconds": metric.duration_seconds,
                "provider_used": metric.provider_used
            }) + "\n")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get aggregate statistics.

        Returns:
            Dict with success rate, avg duration, etc.
        """
        if not self._history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "avg_duration_seconds": 0.0
            }

        successful = sum(1 for m in self._history if m.success)
        durations = [m.duration_seconds for m in self._history if m.duration_seconds]

        return {
            "total_executions": len(self._history),
            "successful": successful,
            "failed": len(self._history) - successful,
            "success_rate": successful / len(self._history),
            "avg_duration_seconds": sum(durations) / len(durations) if durations else 0.0,
            "min_duration_seconds": min(durations) if durations else 0.0,
            "max_duration_seconds": max(durations) if durations else 0.0
        }

    def get_recent(self, limit: int = 10) -> List[ExecutionMetric]:
        """Get most recent executions."""
        return self._history[-limit:]
