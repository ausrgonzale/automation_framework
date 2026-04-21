from typing import Dict, List

from mcp.base.tool import MCPTool


class MCPRegistry:
    """
    Central registry for all MCP tools.

    Responsibilities:
    - Register tools
    - Retrieve tools by name
    - List available tools
    - Prevent duplicate registrations
    """

    def __init__(self) -> None:
        self._tools: Dict[str, MCPTool] = {}

    def register(self, tool: MCPTool) -> None:
        """
        Register a tool instance.

        Args:
            tool: MCPTool instance

        Raises:
            ValueError if tool already registered
        """

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> MCPTool:
        """
        Retrieve a tool by name.

        Args:
            name: Tool name

        Returns:
            MCPTool instance

        Raises:
            ValueError if tool not found
        """

        try:
            return self._tools[name]

        except KeyError as exc:
            available = ", ".join(
                sorted(self._tools.keys())
            )

            raise ValueError(
                f"Tool not found: {name}. "
                f"Available tools: {available}"
            ) from exc

    def list_tools(self) -> List[str]:
        """
        Return list of registered tool names.
        """

        return sorted(self._tools.keys())

    def is_registered(self, name: str) -> bool:
        """
        Check if a tool is registered.
        """

        return name in self._tools

    def clear(self) -> None:
        """
        Clear registry.

        Primarily used for testing.
        """

        self._tools.clear()

    def __len__(self) -> int:
        """
        Allow len(registry).
        """

        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        """
        Allow:

        if "read_file" in registry:
        """

        return name in self._tools