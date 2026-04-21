"""
===============================================================================
File: base_agent.py

Location:
    ai/agents/

Component Type:
    Base Agent

Purpose:
    Provides shared runtime behavior for all agents.

Responsibilities:

    - Provider selection (ollama / openai / anthropic)
    - Model configuration
    - Retry handling
    - Message management
    - Memory protection
    - Logging
    - Safe runtime defaults

All agents must inherit from BaseAgent.

===============================================================================
"""

import logging
import time

from typing import Any, Dict, List, Optional

from ai.client_factory import get_ai_client


logger = logging.getLogger(__name__)


class BaseAgent:
    """
    Base class for all agents.

    Child agents inherit:

        provider configuration
        retry logic
        message handling
        memory protection
    """

    # ------------------------------------------------------------------
    # Explicit attribute declarations (fixes Pylance inheritance issues)
    # ------------------------------------------------------------------

    messages: List[Dict[str, Any]]
    provider: str
    model: str
    max_tokens: int
    max_messages: int
    client: Any

    # ------------------------------------------------------------------
    # Defaults
    # ------------------------------------------------------------------

    DEFAULT_PROVIDER = "ollama"

    DEFAULT_MODELS = {
        "ollama": "qwen2.5-coder:latest",
        "openai": "gpt-4o",
        "anthropic": "claude-sonnet-4-5",
    }

    DEFAULT_MAX_TOKENS = 2048
    DEFAULT_MAX_MESSAGES = 10

    # ------------------------------------------------------------------

    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_messages: Optional[int] = None,
    ) -> None:

        self.provider = provider or self.DEFAULT_PROVIDER

        self.model = (
            model
            or self.DEFAULT_MODELS.get(
                self.provider,
                "qwen2.5-coder:7b",
            )
        )

        self.max_tokens = (
            max_tokens
            or self.DEFAULT_MAX_TOKENS
        )

        self.max_messages = (
            max_messages
            or self.DEFAULT_MAX_MESSAGES
        )

        # Create provider-specific client

        self.client = get_ai_client(
            provider=self.provider
        )

        # Message history

        self.messages = []

        logger.info(
            "Agent initialized",
            extra={
                "provider": self.provider,
                "model": self.model,
                "max_tokens": self.max_tokens,
                "max_messages": self.max_messages,
            },
        )

    # ------------------------------------------------------------------

    def _trim_messages(self) -> None:
        """
        Prevent unbounded memory growth.
        """

        if len(self.messages) > self.max_messages:

            self.messages = self.messages[
                -self.max_messages :
            ]

    # ------------------------------------------------------------------

    def _call_model(
        self,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Any:
        """
        Execute model request.

        Handles:

            provider routing
            retry behavior
            memory trimming

        Supports:

            Ollama
            OpenAI
            Anthropic
        """

        self._trim_messages()

        for attempt in range(3):

            try:

                # -----------------------------
                # Anthropic
                # -----------------------------

                if self.provider == "anthropic":

                    return self.client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        messages=self.messages,
                        tools=tools,
                    )

                # -----------------------------
                # OpenAI / Ollama
                # -----------------------------

                return self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=self.messages,
                    tools=tools,
                )

            except Exception as e:

                wait = 10 * (attempt + 1)

                logger.warning(
                    "Retrying model call",
                    extra={
                        "attempt": attempt + 1,
                        "wait_seconds": wait,
                        "error": str(e),
                    },
                )

                time.sleep(wait)

        raise RuntimeError(
            "Exceeded retry attempts"
        )