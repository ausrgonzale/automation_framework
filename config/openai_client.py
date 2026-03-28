import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_openai_client() -> OpenAI:
    """
    Create and return a configured OpenAI client.

    Centralized configuration ensures:
    - consistent timeout behavior
    - retry handling
    - environment validation
    - shared configuration across agents
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment")
        raise RuntimeError(
            "OPENAI_API_KEY not found in environment variables"
        )

    timeout = int(os.getenv("OPENAI_TIMEOUT", "30"))
    max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "3"))

    logger.info("Initializing OpenAI client")
    logger.debug(
        "OpenAI configuration: timeout=%s, retries=%s",
        timeout,
        max_retries,
    )

    return OpenAI(
        api_key=api_key,
        timeout=timeout,
        max_retries=max_retries,
    )