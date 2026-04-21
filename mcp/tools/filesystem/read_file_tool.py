from pathlib import Path
import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class ReadFileTool(MCPTool):
    """
    Tool for reading file contents.
    """

    name = "read_file"

    def execute(
        self,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:

        path = arguments["path"]

        try:

            logger.info(
                "Reading file: %s",
                path,
            )

            content = Path(path).read_text()

            return {
                "status": "success",
                "content": content,
            }

        except Exception as e:

            logger.error(
                "File read failed: %s",
                e,
            )

            return {
                "status": "error",
                "message": str(e),
            }