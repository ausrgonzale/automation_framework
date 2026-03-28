import logging
from typing import Callable, Dict, Any

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Central registry for all tools.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._schemas: Dict[str, dict] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        schema: dict,
    ) -> None:

        logger.info("Registering tool: %s", name)

        self._tools[name] = handler
        self._schemas[name] = schema

    def get_tool_schemas(self) -> list[dict]:

        return [
            {
                "name": name,
                "description": f"{name} tool",
                "input_schema": schema,
            }
            for name, schema in self._schemas.items()
        ]
    
    def execute(
        self,
        name: str,
        arguments: dict,
    ) -> str:

        if name not in self._tools:

            logger.warning("Unknown tool: %s", name)

            return f"Unknown tool: {name}"

        try:

            handler = self._tools[name]

            return handler(arguments)

        except Exception as e:

            logger.error("Tool execution failed: %s", e)

            return f"Tool execution error: {e}"
        
    def list_tools(self) -> list[str]:

        return list(self._tools.keys())


tool_registry = ToolRegistry()