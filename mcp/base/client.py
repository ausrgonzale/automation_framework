from typing import Any, Dict

from mcp.base.registry import MCPRegistry


class MCPClient:
    """
    Client used by agents to call MCP tools.
    """

    def __init__(self, registry: MCPRegistry) -> None:
        self.registry = registry

    def call_tool(
        self,
        name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a registered tool.
        """

        tool = self.registry.get_tool(name)

        return tool.execute(arguments)