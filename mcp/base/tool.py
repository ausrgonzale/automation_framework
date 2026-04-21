from abc import ABC, abstractmethod
from typing import Any, Dict


class MCPTool(ABC):
    """
    Base class for all MCP tools.
    """

    name: str

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool.

        Returns:
            Dict response payload
        """
        pass