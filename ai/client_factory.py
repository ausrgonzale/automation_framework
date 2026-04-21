"""
===============================================================================
File: client_factory.py

Location:
    ai/

Purpose:

    Centralized creation of AI provider clients.

Returns:

    Provider instances implementing:

        generate(prompt: str) -> str

===============================================================================
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv

from ai.providers.ollama_provider import OllamaProvider
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.anthropic_provider import AnthropicProvider


# Load environment variables from .env file
load_dotenv()


logger = logging.getLogger(__name__)


DEFAULT_PROVIDER = "ollama"


def get_ai_client(
    provider: Optional[str] = None,
):
    """
    Create and return an AI provider instance.
    """

    provider = (
        provider
        or os.getenv("AI_PROVIDER")
        or DEFAULT_PROVIDER
    )

    logger.info(
        "Creating AI client",
        extra={
            "provider": provider
        },
    )

    if provider == "ollama":
        return _create_ollama_client()

    if provider == "openai":
        return _create_openai_client()

    if provider == "anthropic":
        return _create_anthropic_client()

    raise ValueError(
        f"Unsupported provider: {provider}"
    )


# ---------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------

def _create_ollama_client():

    model = os.getenv(
        "AI_MODEL",
        "MFDoom/deepseek-r1-tool-calling:latest",
    )

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    timeout = int(
        os.getenv(
            "AI_TIMEOUT",
            "300",  # Increased from 120 to 300 seconds
        )
    )

    logger.info(
        "Initializing Ollama provider",
        extra={
            "model": model,
            "base_url": base_url,
            "timeout": timeout,
        },
    )

    return OllamaProvider(
        model=model,
        base_url=base_url,
        timeout=timeout,
    )


# ---------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------

def _create_openai_client():

    model = os.getenv(
        "AI_MODEL",
        "gpt-4o-mini",
    )

    logger.info(
        "Initializing OpenAI provider",
        extra={
            "model": model,
        },
    )

    return OpenAIProvider(
        model=model,
    )


# ---------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------

def _create_anthropic_client():

    model = os.getenv(
        "AI_MODEL",
        "claude-3-5-sonnet-latest",
    )

    logger.info(
        "Initializing Anthropic provider",
        extra={
            "model": model,
        },
    )

    return AnthropicProvider(
        model=model,
    )