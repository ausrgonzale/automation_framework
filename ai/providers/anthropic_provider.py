import os
import json
import logging
import httpx
import anthropic
from dotenv import load_dotenv
from typing import Any

from .base import AIProvider
from ai.utils.retry import retry_call
from ai.schemas.tool_call import StandardToolCall

load_dotenv()

logger = logging.getLogger(__name__)


class AnthropicProvider(AIProvider):
    """
    Anthropic provider implementation.

    Centralized configuration ensures:
    - consistent timeout behavior
    - retry handling
    - environment validation
    - shared configuration across agents
    """

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-latest",
    ):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            logger.error("ANTHROPIC_API_KEY not found in environment")
            raise RuntimeError(
                "ANTHROPIC_API_KEY not found in environment variables"
            )

        read_timeout = int(
            os.getenv("ANTHROPIC_READ_TIMEOUT", "600")
        )
        connect_timeout = int(
            os.getenv("ANTHROPIC_CONNECT_TIMEOUT", "10")
        )
        max_retries = int(
            os.getenv("ANTHROPIC_MAX_RETRIES", "3")
        )

        timeout = httpx.Timeout(
            connect=connect_timeout,
            read=read_timeout,
            write=10.0,
            pool=10.0,
        )

        logger.info("Initializing Anthropic provider")
        logger.debug(
            "Anthropic configuration: read_timeout=%s, connect_timeout=%s, retries=%s",
            read_timeout,
            connect_timeout,
            max_retries,
        )

        self.client = anthropic.Anthropic(
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

        kwargs = {}

        # Only include system if provided
        if system is not None:
            kwargs["system"] = system

        response = retry_call(
            lambda: self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                **kwargs,
                
            )
        )

        text_parts: list[str] = []

        # Safely extract text blocks
        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)

        if not text_parts:
            logger.error(
                "Anthropic response contained no text blocks"
            )
            raise RuntimeError(
                "Anthropic response contained no text blocks"
            )

        return "\n".join(text_parts)

    def normalize_response(
        self,
        response: Any,
    ) -> list[StandardToolCall]:
        """
        Parse Anthropic's response format.
        
        For consistency with the framework, Anthropic is expected to return
        the same JSON structure as Ollama (plain tools array):
        {
            "tools": [
                {"name": "write", "arguments": {"path": "...", "content": "..."}},
                {"name": "bash", "arguments": {"command": "..."}}
            ]
        }
        
        This method handles:
        - JSON parsing of string responses
        - Validation of tool entries
        - Type checking for names and arguments
        
        Args:
            response: String response from Anthropic API
            
        Returns:
            List of StandardToolCall objects
            
        Implementation Notes:
            - Anthropic also supports tool_use blocks natively
            - This implementation standardizes to the tools array format
            - Gracefully handles missing/malformed entries
            - All errors logged; never raises exceptions
            
        Future Enhancement:
            Could be extended to parse Anthropic's native tool_use blocks
            directly without requiring JSON wrapper in the prompt.
        """

        if not isinstance(response, str):
            logger.warning("Anthropic response is not a string")
            return []

        try:
            response_data = json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Anthropic response is not valid JSON")
            return []

        tools = response_data.get("tools")

        if not isinstance(tools, list):
            logger.warning("No tools array in Anthropic response")
            return []

        calls: list[StandardToolCall] = []

        for tool in tools:
            if not isinstance(tool, dict):
                logger.warning("Tool entry is not a dict")
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

        logger.info("Normalized %d tool calls from Anthropic", len(calls))
        return calls