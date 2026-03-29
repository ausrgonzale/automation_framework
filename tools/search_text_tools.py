from pathlib import Path
import logging
from pydantic import BaseModel

from tools.tool_registry import tool_registry

logger = logging.getLogger(__name__)


class SearchTextArgs(BaseModel):
    path: str
    pattern: str

def search_file(file_path: Path, pattern: str) -> list[str]:

    matches = []

    try:

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):

            if pattern in line:

                matches.append(
                    f"{file_path}:{line_number}: {line}"
                )

    except Exception as e:

        logger.debug(
            "Skipping unreadable file %s: %s",
            file_path,
            e,
        )

    return matches

def execute_search_text(args: SearchTextArgs) -> str:

    try:

        path = Path(args.path)

        if not path.exists():

            return f"Path not found: {args.path}"

        matches = []

        if path.is_file():

            matches.extend(
                search_file(path, args.pattern)
            )

        else:

            for file_path in path.rglob("*"):

                if any(
                    part.startswith(".")
                    or part == "__pycache__"
                    for part in file_path.parts
                ):
                    continue

                if file_path.is_file():

                    matches.extend(
                        search_file(
                            file_path,
                            args.pattern,
                        )
                    )

        if not matches:

            return "No matches found"

        return "\n".join(matches)

    except Exception as e:

        logger.error("Search failed: %s", e)

        return f"Search error: {e}"


tool_registry.register(
    name="search_text",
    handler=lambda args: execute_search_text(
        SearchTextArgs.model_validate(args)
    ),
    schema=SearchTextArgs.model_json_schema(),
)