from pathlib import Path
import logging
from pydantic import BaseModel

from tools.tool_registry import tool_registry

logger = logging.getLogger(__name__)


class WriteFileArgs(BaseModel):
    path: str
    content: str


def execute_write_file(args: WriteFileArgs) -> str:

    try:

        file_path = Path(args.path)

        file_path.write_text(args.content)

        logger.info("File written: %s", args.path)

        return f"File written: {args.path}"

    except Exception as e:

        logger.error("File write failed: %s", e)

        return f"File write error: {e}"


tool_registry.register(
    name="write_file",
    handler=lambda args: execute_write_file(
        WriteFileArgs.model_validate(args)
    ),
    schema=WriteFileArgs.model_json_schema(),
)