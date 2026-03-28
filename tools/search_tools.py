import os
import requests
import logging
from dotenv import load_dotenv
from pydantic import BaseModel

from tools.tool_registry import tool_registry

load_dotenv()

logger = logging.getLogger(__name__)

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")


class SearchArgs(BaseModel):
    """Search the web for information."""
    query: str


def execute_search(args: SearchArgs) -> str:
    """
    Execute a web search and return formatted results.
    """

    if not SEARCH_API_KEY:
        logger.error("SEARCH_API_KEY not found")
        return "Search error: API key not configured"

    try:

        logger.info("Executing search")

        response = requests.get(
            "https://api.serper.dev/search",
            headers={
                "X-API-KEY": SEARCH_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "q": args.query,
                "num": 5,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("organic", []):

            results.append(
                f"{item.get('title')}\n"
                f"{item.get('link')}\n"
                f"{item.get('snippet')}\n"
            )

        logger.info("Search completed")

        if not results:
            return "No results found."

        return "\n\n".join(results)

    except Exception as e:

        logger.error("Search failed: %s", e)

        return f"Search error: {e}"


# Register the tool AFTER the function is defined

tool_registry.register(
    name="search",
    handler=lambda args: execute_search(
        SearchArgs.model_validate(args)
    ),
    schema=SearchArgs.model_json_schema(),
)