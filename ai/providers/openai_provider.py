import os
import json
import logging
from typing import cast, Any

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from .base import AIProvider
from ai.utils.retry import retry_call
from ai.schemas.tool_call import StandardToolCall

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """
    OpenAI provider implementation.

    Centralized configuration ensures:
    - consistent timeout behavior
    - retry handling
    - environment validation
    - shared configuration across agents
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
    ):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            logger.error(
                "OPENAI_API_KEY not found in environment"
            )
            raise RuntimeError(
                "OPENAI_API_KEY not found in environment variables"
            )

        timeout = int(
            os.getenv("OPENAI_TIMEOUT", "30")
        )
        max_retries = int(
            os.getenv("OPENAI_MAX_RETRIES", "3")
        )

        logger.info("Initializing OpenAI provider")
        logger.debug(
            "OpenAI configuration: timeout=%s, retries=%s",
            timeout,
            max_retries,
        )

        self.client = OpenAI(
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.model = model

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a response from the OpenAI model.

        Always returns a string or raises RuntimeError.
        """

        messages: list[ChatCompletionMessageParam] = []

        if system is not None:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = retry_call(
            lambda: self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        )

        # OpenAI SDK type: str | None
        content = response.choices[0].message.content

        if content is None:
            logger.error(
                "OpenAI returned empty response content"
            )
            raise RuntimeError(
                "OpenAI response content is empty"
            )

        # Explicit cast satisfies strict type checkers
        return cast(str, content)

    def normalize_response(
        self,
        response: Any,
    ) -> list[StandardToolCall]:
        """
        Parse OpenAI's response format with tool_calls.
        
        OpenAI returns responses in the OpenAI format:
        {
            "choices": [
                {
                    "message": {
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "function": {
                                    "name": "write",
                                    "arguments": "{\\"path\\": \\"...\\", \\"content\\": \\"...\\"}"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        This method handles:
        - JSON response parsing
        - Nested structure extraction (choices -> message -> tool_calls)
        - Arguments which may be JSON strings (parses them to dicts)
        - Type validation and error recovery
        
        Args:
            response: Either raw JSON string or dict from OpenAI API
            
        Returns:
            List of StandardToolCall objects
            
        Implementation Notes:
            - OpenAI returns arguments as JSON strings, not dicts
            - Must parse arguments JSON separately
            - Gracefully handles missing/malformed entries
            - All errors logged; never raises exceptions
            - Compatible with OpenAI SDK responses
            
        Error Handling:
            - Non-string response: warns and returns empty list
            - Invalid JSON: warns and returns empty list
            - Wrong structure: warns and returns empty list
            - Invalid entries: skipped with warning, continues processing
        """

        if not isinstance(response, str):
            logger.warning("OpenAI response is not a string")
            return []

        try:
            response_data = json.loads(response)
        except json.JSONDecodeError:
            logger.warning("OpenAI response is not valid JSON")
            return []

        choices = response_data.get("choices")

        if not isinstance(choices, list) or not choices:
            logger.warning("No choices in OpenAI response")
            return []

        message = choices[0].get("message", {})
        tool_calls = message.get("tool_calls")

        if not isinstance(tool_calls, list):
            logger.warning("No tool_calls in OpenAI response")
            return []

        calls: list[StandardToolCall] = []

        for tool_call in tool_calls:
            if not isinstance(tool_call, dict):
                logger.warning("Tool call entry is not a dict")
                continue

            function = tool_call.get("function", {})

            if not isinstance(function, dict):
                logger.warning("Function is not a dict")
                continue

            name = function.get("name")
            arguments_str = function.get("arguments", "{}")

            if not isinstance(name, str) or not name:
                logger.warning("Tool call missing or invalid name")
                continue

            try:
                if isinstance(arguments_str, str):
                    arguments = json.loads(arguments_str)
                else:
                    arguments = arguments_str if isinstance(arguments_str, dict) else {}
            except json.JSONDecodeError:
                logger.warning("Failed to parse arguments JSON")
                arguments = {}

            calls.append(
                StandardToolCall(
                    name=name,
                    arguments=arguments,
                )
            )

        logger.info("Normalized %d tool calls from OpenAI", len(calls))
        return calls