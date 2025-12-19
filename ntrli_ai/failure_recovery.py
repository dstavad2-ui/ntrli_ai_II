# ============================================================================
# NTRLI' AI - FAILURE RECOVERY & OFFLINE RESILIENCE
# ============================================================================
"""
Failure recovery module with retry logic.

BEHAVIORAL LAW: No silent failure.

If an operation fails:
1. Retry up to MAX_RETRIES times
2. If all retries fail, raise an explicit error
3. Never swallow exceptions silently
"""

from typing import Callable, TypeVar, Optional
import time

T = TypeVar('T')


class RecoveryError(RuntimeError):
    """Raised when recovery fails after all retries."""
    pass


class FailureRecovery:
    """
    Failure recovery with bounded retry logic.

    Provides deterministic retry behavior with no infinite loops.
    """

    MAX_RETRIES = 2
    RETRY_DELAY_SECONDS = 1.0

    def should_retry(self, attempt: int) -> bool:
        """
        Determine if another retry should be attempted.

        Args:
            attempt: Current attempt number (1-indexed)

        Returns:
            True if should retry, False otherwise
        """
        return attempt < self.MAX_RETRIES

    def retry(
        self,
        func: Callable[[], T],
        description: str = "operation"
    ) -> T:
        """
        Execute function with retry logic.

        Args:
            func: Function to execute
            description: Description for error messages

        Returns:
            Result of successful function call

        Raises:
            RecoveryError: If all retries fail
        """
        attempt = 0
        last_error: Optional[Exception] = None
        errors: list[str] = []

        while True:
            attempt += 1
            try:
                return func()
            except Exception as e:
                last_error = e
                errors.append(f"Attempt {attempt}: {type(e).__name__}: {e}")

                if not self.should_retry(attempt):
                    break

                # Wait before retry
                time.sleep(self.RETRY_DELAY_SECONDS)

        # All retries exhausted
        error_log = "\n".join(errors)
        raise RecoveryError(
            f"Failed {description} after {attempt} attempts:\n{error_log}"
        ) from last_error

    def retry_with_backoff(
        self,
        func: Callable[[], T],
        description: str = "operation",
        base_delay: float = 1.0,
        max_delay: float = 30.0
    ) -> T:
        """
        Execute function with exponential backoff retry.

        Args:
            func: Function to execute
            description: Description for error messages
            base_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds

        Returns:
            Result of successful function call

        Raises:
            RecoveryError: If all retries fail
        """
        attempt = 0
        last_error: Optional[Exception] = None
        errors: list[str] = []

        while True:
            attempt += 1
            try:
                return func()
            except Exception as e:
                last_error = e
                errors.append(f"Attempt {attempt}: {type(e).__name__}: {e}")

                if not self.should_retry(attempt):
                    break

                # Exponential backoff with cap
                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                time.sleep(delay)

        error_log = "\n".join(errors)
        raise RecoveryError(
            f"Failed {description} after {attempt} attempts:\n{error_log}"
        ) from last_error
