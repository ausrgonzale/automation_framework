from pathlib import Path
import logging
from pydantic import BaseModel

from tools.tool_registry import tool_registry

logger = logging.getLogger(__name__)


class AppendFileArgs(BaseModel):
    path: str
    content: str


def execute_append_file(args: AppendFileArgs) -> str:

    try:

        file_path = Path(args.path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with file_path.open(
            "a",
            encoding="utf-8",
        ) as f:

            f.write(args.content)

            if not args.content.endswith("\n"):
                f.write("\n")

        logger.info(
            "Content appended to file: %s",
            args.path,
        )

        return f"Content appended to file: {args.path}"

    except Exception as e:

        logger.error(
            "File append failed: %s",
            e,
        )

        return f"File append error: {e}"


tool_registry.register(
    name="append_file",
    handler=lambda args: execute_append_file(
        AppendFileArgs.model_validate(args)
    ),
    schema=AppendFileArgs.model_json_schema(),
)