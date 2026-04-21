from pathlib import Path
import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class WriteFileTool(MCPTool):

    name = "write_file"

    def execute(
        self,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:

        path = arguments["path"]
        content = arguments["content"]

        try:

            file_path = Path(path)

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path.write_text(
                content,
                encoding="utf-8",
            )

            logger.info(
                "File written: %s",
                path,
            )

            return {
                "status": "success",
                "path": str(file_path),
                "bytes_written": len(content),
            }

        except Exception as e:

            logger.error(
                "File write failed: %s",
                e,
            )

            return {
                "status": "error",
                "message": str(e),
            }