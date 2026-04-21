"""
===============================================================================
File: ai_client.py

Location:
    ai/

Component Type:
    Unified AI Client

Purpose:

    Provide a provider-agnostic interface for generating text.

Design Principles:

    - Single interface across providers
    - Hide SDK-specific APIs
    - Stable contract for agents and tests
    - Environment-driven configuration

===============================================================================
"""

import logging
from typing import Any


logger = logging.getLogger(__name__)


class AIClient:
    """
    Unified AI client wrapper.

    All providers expose:

        generate_text(prompt)
    """

    def __init__(
        self,
        provider: str,
        client: Any,
        model: str,
    ):

        self.provider = provider
        self.client = client
        self.model = model

        logger.info(
            "AIClient initialized",
            extra={
                "provider": provider,
                "model": model,
            },
        )

    # -----------------------------------------------------------------

    def generate_text(
        self,
        prompt: str,
        *,
        temperature: float = 0,
        max_output_tokens: int = 300,
        timeout: int = 30,
    ) -> str:

        logger.info(
            "Generating text",
            extra={
                "provider": self.provider,
            },
        )

        # -------------------------------------------------------------
        # Ollama / OpenAI
        # -------------------------------------------------------------

        if self.provider in ("ollama", "openai"):

            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                timeout=timeout,
            )

            return response.output_text

        # -------------------------------------------------------------
        # Anthropic
        # -------------------------------------------------------------

        if self.provider == "anthropic":

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_output_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response.content[0].text

        # -------------------------------------------------------------

        raise ValueError(
            f"Unsupported provider: {self.provider}"
        )