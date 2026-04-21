import json
import logging
import os

import requests

from ai.schemas.tool_call import StandardToolCall
from ai.utils.retry import retry_call

from .base import AIProvider

logger = logging.getLogger(__name__)


class OllamaProvider(AIProvider):
    """
    Local Ollama provider implementation.
    """

    def __init__(
        self,
        model: str = "llama3.1:latest",
        base_url: str | None = None,
        timeout: int | None = None,
    ):
        self.model = model

        self.base_url = base_url or os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        )

        if self.base_url.endswith("/v1"):
            self.base_url = self.base_url[: -len("/v1")]

        self.base_url = self.base_url.rstrip("/")

        self.timeout = timeout or int(os.getenv("OLLAMA_TIMEOUT", "60"))

        logger.info("Initializing Ollama provider")
        logger.debug(
            "Ollama configuration: model=%s, base_url=%s, timeout=%s",
            self.model,
            self.base_url,
            self.timeout,
        )

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        stop: list | None = None,
    ) -> str:

        url = f"{self.base_url}/api/generate"

        options = {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
        if stop:
            options["stop"] = stop

        payload: dict[str, object] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }

        if system is not None:
            payload["system"] = system

        response = retry_call(
            lambda: requests.post(
                url,
                json=payload,
                timeout=self.timeout,
            )
        )

        response.raise_for_status()

        data = response.json()

        content = data.get("response")

        if not isinstance(content, str):
            logger.error("Ollama returned invalid response content")
            raise RuntimeError("Ollama response content is invalid")

        return content

    def normalize_response(
        self,
        response: str,
    ) -> list[StandardToolCall]:
        """
        Parse Ollama's plain text JSON response containing tool calls.

        Ollama returns responses as plain text JSON in this format:
        {
            "tools": [
                {"name": "write", "arguments": {"path": "...", "content": "..."}},
                {"name": "bash", "arguments": {"command": "..."}}
            ]
        }

        This method handles:
        - JSON parsing errors (logs warning, returns empty list)
        - Missing or malformed tool entries (skips invalid ones)
        - Type validation for name and arguments

        Args:
            response: Raw string response from Ollama's /api/generate endpoint

        Returns:
            List of StandardToolCall objects ready for agents to consume

        Implementation Notes:
            - Ollama requires explicit JSON structure in the prompt
            - See scripts/generate_tests.py for the prompt format
            - All errors are logged for debugging; never raises exceptions
            - Invalid entries are skipped, not failed-fast
        """

        try:
            response_data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            logger.warning("Ollama response is not valid JSON")
            return []

        tools = response_data.get("tools")

        if not isinstance(tools, list):
            logger.warning("No tools array in Ollama response")
            return []

        calls: list[StandardToolCall] = []

        for tool in tools:
            if not isinstance(tool, dict):
                logger.warning("Tool entry is not a dict: %s", tool)
                continue

            name = tool.get("name")
            arguments = tool.get("arguments", {})

            if not isinstance(name, str) or not name:
                logger.warning("Tool missing or invalid name")
                continue

            if not isinstance(arguments, dict):
                logger.warning("Tool arguments is not a dict")
                continue

            calls.append(
                StandardToolCall(
                    name=name,
                    arguments=arguments,
                )
            )

        logger.info("Normalized %d tool calls from Ollama", len(calls))
        return calls
