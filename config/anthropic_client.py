import os
import logging
import httpx
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

    read_timeout = int(os.getenv("ANTHROPIC_READ_TIMEOUT", "600"))
    connect_timeout = int(os.getenv("ANTHROPIC_CONNECT_TIMEOUT", "10"))
    max_retries = int(os.getenv("ANTHROPIC_MAX_RETRIES", "3"))

    timeout = httpx.Timeout(
        connect=connect_timeout,  # time to establish connection
        read=read_timeout,        # time to wait for model response — the one expiring
        write=10.0,
        pool=10.0,
    )

    logger.info("Initializing Anthropic client")
    logger.debug(
        "Anthropic configuration: read_timeout=%s, connect_timeout=%s, retries=%s",
        read_timeout,
        connect_timeout,
        max_retries,
    )

    return anthropic.Anthropic(
        api_key=api_key,
        timeout=timeout,
        max_retries=max_retries,
    )