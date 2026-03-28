import os
import logging
import anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_anthropic_client() -> anthropic.Anthropic:
    """
    Create and return a configured Anthropic client.

    Centralized configuration ensures:
    - consistent timeout behavior
    - retry handling
    - environment validation
    - shared configuration across agents
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        logger.error("ANTHROPIC_API_KEY not found in environment")
        raise RuntimeError(
            "ANTHROPIC_API_KEY not found in environment variables"
        )

    timeout = int(os.getenv("ANTHROPIC_TIMEOUT", "30"))
    max_retries = int(os.getenv("ANTHROPIC_MAX_RETRIES", "3"))

    logger.info("Initializing Anthropic client")
    logger.debug(
        "Anthropic configuration: timeout=%s, retries=%s",
        timeout,
        max_retries,
    )

    return anthropic.Anthropic(
        api_key=api_key,
        timeout=timeout,
        max_retries=max_retries,
    )