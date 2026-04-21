"""
===============================================================================
File: file_exists_tool.py

Location:
    mcp/tools/filesystem/

Component Type:
    MCP Tool

Purpose:
    Provides a safe, deterministic way to check whether a file or directory
    exists on the filesystem.

Architecture Role:
    Part of the Filesystem Capability Layer within the MCP (Model Control
    Plane). This tool is executed through the MCP client and registry.

Interface Contract:
    execute(arguments: Dict[str, Any]) -> Dict[str, Any]

===============================================================================
"""

from pathlib import Path
from typing import Any, Dict
import logging

from mcp.base.tool import MCPTool


logger = logging.getLogger(__name__)


class FileExistsTool(MCPTool):
    """
    MCP Tool implementation for checking filesystem existence.
    """

    name = "file_exists"

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine whether the provided path exists.
        """

        if not isinstance(arguments, dict):
            raise TypeError("arguments must be a dictionary")

        path = arguments.get("path")

        if not path:
            raise ValueError("Missing required argument: path")

        logger.info(
            "Checking if path exists",
            extra={
                "path": path,
            },
        )

        try:
            exists = Path(path).exists()

            logger.info(
                "File existence result",
                extra={
                    "path": path,
                    "exists": exists,
                },
            )

            return {
                "exists": exists
            }

        except Exception:
            logger.exception(
                "file_exists failed",
                extra={
                    "path": path,
                },
            )
            raise