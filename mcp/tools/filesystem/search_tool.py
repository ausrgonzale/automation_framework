from pathlib import Path
import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class SearchFilesTool(MCPTool):

    name = "search_files"

    def execute(
        self,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:

        path = arguments["path"]
        pattern = arguments["pattern"]

        try:

            base_path = Path(path)

            if not base_path.exists():

                return {
                    "status": "error",
                    "message": f"Path not found: {path}",
                }

            matches = [
                str(p)
                for p in base_path.rglob(pattern)
            ]

            return {
                "status": "success",
                "matches": matches,
                "count": len(matches),
            }

        except Exception as e:

            logger.error(
                "File search failed: %s",
                e,
            )

            return {
                "status": "error",
                "message": str(e),
            }