from pathlib import Path
import logging
from pydantic import BaseModel

from tools.tool_registry import tool_registry

logger = logging.getLogger(__name__)


class ListDirectoryArgs(BaseModel):
    path: str

def execute_list_directory(args: ListDirectoryArgs) -> str:

    try:

        directory = Path(args.path)

        if not directory.exists():

            return f"Directory not found: {args.path}"

        if not directory.is_dir():

            return f"Not a directory: {args.path}"

        items = sorted(p.name for p in directory.iterdir())

        if not items:

            return "Directory is empty"

        return "\n".join(items)

    except Exception as e:

        logger.error("Directory listing failed: %s", e)

        return f"Directory listing error: {e}"


tool_registry.register(
    name="list_directory",
    handler=lambda args: execute_list_directory(
        ListDirectoryArgs.model_validate(args)
    ),
    schema=ListDirectoryArgs.model_json_schema(),
)