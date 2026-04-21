from __future__ import annotations

"""
===============================================================================
File: coding_agent.py

Purpose:
    Production-ready Coding Agent responsible for interacting with the AI model
    and collecting tool operations in a deterministic and controlled manner.

Key Design Goals:

    - Single-pass execution (no autonomous loops)
    - Deterministic orchestration
    - Safe for CI/CD environments
    - Predictable CPU usage (important for local LLMs like Ollama)
    - Clear logging for debugging and onboarding developers

This version preserves a full-featured structure suitable for your automation
framework while enforcing the architectural change you requested:

    Cache operations -> return operations -> execute once

The agent NEVER executes tools directly.
That responsibility belongs to the orchestration layer.

===============================================================================
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
# =============================================================================
# Constants
# =============================================================================


DEFAULT_TEMPERATURE = 0
DEFAULT_STREAM = False


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class ToolOperation:
    """
    Represents a tool call requested by the AI model.

    This object is intentionally simple and serializable.
    """

    name: str
    arguments: Dict[str, Any]


@dataclass
class AgentResponse:
    """
    Structured response returned by the agent.
    """

    operations: List[ToolOperation]
    raw_response: Any


# =============================================================================
# Coding Agent
# =============================================================================


class CodingAgent:
    """
    Coding Agent responsible for generating tool operations.

    Simplified Design (Post-Normalization):
        This agent is intentionally simple. It no longer parses provider
        responses. Instead, it delegates response parsing to the provider's
        normalize_response() method, which returns StandardToolCall objects.

    Responsibilities:

        - Send prompt to AI client via provider.generate()
        - Request normalized response from provider.normalize_response()
        - Convert normalized calls to ToolOperation objects
        - Return structured operations list

    Non-Responsibilities:

        - Parsing provider-specific response formats
        - Understanding different API response structures
        - Execution or tool invocation
        - Retry logic

    Architecture Flow:

        Prompt
           ↓
        Provider.generate() → Raw Response
           ↓
        Provider.normalize_response() → StandardToolCall[]
           ↓
        CodingAgent (this class) → ToolOperation[]
           ↓
        Orchestrator (generate_tests.py) → Execution

    Design Rationale:
        By delegating response parsing to providers, we achieve:
        1. Provider-agnostic agent code (no if/elif for different APIs)
        2. Easy addition of new providers (no agent modification)
        3. Testable response normalization (mock providers return StandardToolCall)
        4. Clear separation of concerns

    Extension for New Providers:
        To add a new provider (e.g., Claude, Grok, etc.):
        1. Create class inheriting from AIProvider
        2. Implement generate() to call the provider API
        3. Implement normalize_response() to parse their response format
        4. Register in client_factory.py
        5. Agent code remains completely unchanged
    """

    # -------------------------------------------------------------------------

    def __init__(
        self,
        client: Any,
        model: Optional[str] = None,
        temperature: int = DEFAULT_TEMPERATURE,
        stream: bool = DEFAULT_STREAM,
        max_tokens: int = 2000,
        stop: Optional[list] = None,
    ):
        """
        Initialize the CodingAgent.
        """

        self.client = client
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.max_tokens = max_tokens
        self.stop = stop

        logger.info("Agent initialized")

    # -------------------------------------------------------------------------

    def process(
        self, query: str, generation_params: Optional[dict] = None
    ) -> List[ToolOperation]:
        """
        Main entry point for generating operations.

        Execution model:

            Call model once
            Parse tool calls using provider's normalizer
            Return operations once

        No retries.
        No loops.
        """

        logger.info("Processing query")

        response = self._send_request(query, generation_params)

        operations = self._collect_operations(response)

        logger.info("Operations collected: %s", len(operations))

        return operations

    # -------------------------------------------------------------------------

    def _send_request(self, query: str, generation_params: Optional[dict] = None):
        """
        Send request to AI model, supporting all generation parameters.
        """
        try:
            params = generation_params or {}
            temperature = params.get("temperature", self.temperature)
            max_tokens = params.get("num_predict", self.max_tokens)
            stop = params.get("stop", self.stop)
            # Pass stop if supported by provider
            response_text = self.client.generate(
                prompt=query,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
            )
            return response_text
        except Exception as exc:
            logger.exception("Model request failed")
            raise RuntimeError("AI request failed") from exc

    # -------------------------------------------------------------------------

    def _collect_operations(self, response: Any) -> List[ToolOperation]:
        """
        Convert provider's normalized tool calls into ToolOperation objects.

        Delegates response parsing to the provider via normalize_response().
        This ensures provider-specific formats are handled by each provider.
        """

        try:
            # Use the provider's normalizer to get StandardToolCall objects
            standard_calls = self.client.normalize_response(response)

            operations: List[ToolOperation] = []

            for call in standard_calls:
                operation = ToolOperation(
                    name=call.name,
                    arguments=call.arguments,
                )

                operations.append(operation)

                logger.info(
                    "Collected tool operation: %s",
                    operation.name,
                )

            return operations

        except Exception as exc:
            logger.error("Failed to normalize response: %s", exc)
            return []

    # -------------------------------------------------------------------------

    def health_check(self) -> bool:
        """
        Simple connectivity test.
        """

        try:
            response_text = self.client.generate(
                prompt="ping",
                temperature=0,
                max_tokens=1,
            )

            return bool(response_text)

        except Exception:
            return False

    # -------------------------------------------------------------------------

    def describe(self) -> Dict[str, Any]:
        """
        Return diagnostic metadata about the agent.
        """

        return {
            "agent": "CodingAgent",
            "model": self.model,
            "temperature": self.temperature,
            "stream": self.stream,
        }


# =============================================================================
# Utility Functions
# =============================================================================


def summarize_operations(operations: List[ToolOperation]) -> Dict[str, Any]:
    """
    Provide a simple summary of collected operations.
    """

    names = [op.name for op in operations]

    return {
        "operation_count": len(operations),
        "operation_names": names,
    }
