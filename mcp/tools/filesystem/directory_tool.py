from pathlib import Path
import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class ListDirectoryTool(MCPTool):

    name = "list_directory"

    def execute(
        self,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:

        path = arguments["path"]

        try:

            directory = Path(path)

            if not directory.exists():

                return {
                    "status": "error",
                    "message": f"Directory not found: {path}",
                }

            if not directory.is_dir():

                return {
                    "status": "error",
                    "message": f"Not a directory: {path}",
                }

            items = sorted(
                p.name for p in directory.iterdir()
            )

            return {
                "status": "success",
                "items": items,
                "count": len(items),
            }

        except Exception as e:

            logger.error(
                "Directory listing failed: %s",
                e,
            )

            return {
                "status": "error",
                "message": str(e),
            }