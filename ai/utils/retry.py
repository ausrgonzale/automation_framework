import logging
import time
import os
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

def retry_call(
    func: Callable[[], T],
    retries: int | None = None,
    delay: float | None = None,
    backoff: float |None = None,
) -> T:
    
    """
    Retry a function call with exponential backoff.

    Parameters:
        retries: number of retry attempts
        delay: initial delay in seconds
        backoff: multiplier applied after each failure
    """

    retries = retries if retries is not None else int(
        os.getenv("AI_RETRIES", "2")  # Reduced from 3
    )

    delay = delay if delay is not None else float(
        os.getenv("AI_RETRY_DELAY", "5")  # Increased from 1
    )

    backoff = backoff if backoff is not None else float(
        os.getenv("AI_RETRY_BACKOFF", "2")
    )

    attempt = 0
    current_delay = delay

    while True:
        try:
            return func()

        except Exception as exc:
            attempt += 1

            if attempt > retries:
                logger.error(
                    "Retry attempts exhausted",
                    extra={
                        "attempts": attempt, 
                    },
                    exc_info=True,
                )
                raise

            logger.warning(
                "Retrying after failure",
                extra={
                    "attempt": attempt,
                    "delay": current_delay,
                    "error": str(exc),
                },
            )

            time.sleep(current_delay)
            current_delay *= backoff