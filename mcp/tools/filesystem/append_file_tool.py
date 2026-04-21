from pathlib import Path
import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class AppendFileTool(MCPTool):

    name = "append_file"

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

            with file_path.open(
                "a",
                encoding="utf-8",
            ) as f:

                f.write(content)

                if not content.endswith("\n"):
                    f.write("\n")

            logger.info(
                "Content appended to file: %s",
                path,
            )

            return {
                "status": "success",
                "path": str(file_path),
            }

        except Exception as e:

            logger.error(
                "File append failed: %s",
                e,
            )

            return {
                "status": "error",
                "message": str(e),
            }