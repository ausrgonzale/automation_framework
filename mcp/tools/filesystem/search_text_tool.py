from pathlib import Path
import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class SearchTextTool(MCPTool):

    name = "search_text"

    def execute(
        self,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:

        path = arguments["path"]
        text = arguments["text"]

        matches = []

        try:

            file_path = Path(path)

            if not file_path.exists():

                return {
                    "status": "error",
                    "message": f"File not found: {path}",
                }

            for line_number, line in enumerate(
                file_path.read_text().splitlines(),
                start=1,
            ):

                if text in line:

                    matches.append(
                        {
                            "line_number": line_number,
                            "line": line,
                        }
                    )

            return {
                "status": "success",
                "matches": matches,
                "count": len(matches),
            }

        except Exception as e:

            logger.error(
                "Text search failed: %s",
                e,
            )

            return {
                "status": "error",
                "message": str(e),
            }