from pathlib import Path
import logging
from pydantic import BaseModel

from mcp.tools.filesystem.tool_registry import tool_registry

logger = logging.getLogger(__name__)


class ReadFileArgs(BaseModel):
    path: str


def execute_read_file(args: ReadFileArgs) -> str:

    try:

        logger.info("Reading file: %s", args.path)

        return Path(args.path).read_text()

    except Exception as e:

        logger.error("File read failed: %s", e)

        return f"File read error: {e}"


tool_registry.register(
    name="read_file",
    handler=lambda args: execute_read_file(
        ReadFileArgs.model_validate(args)
    ),
    schema=ReadFileArgs.model_json_schema(),
)