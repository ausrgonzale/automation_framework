import logging

from config.logging_config import configure_logging

from tools.tool_registry import tool_registry
from tools import file_tools
from tools import directory_tools
from tools import write_file_tools


# Configure logging once at startup
configure_logging()

logger = logging.getLogger(__name__)


def show_startup_help() -> None:
    """
    Display startup banner and available commands.
    """

    print("\nSearch Agent started\n")

    tools = tool_registry.list_tools()

    print("Available commands:\n")

    for tool in tools:
        print(f"  {tool} <path>")
        print(f"      Example: {tool} README.md\n")

    print("Type 'help' to see this list again.")
    print("Type 'exit' or 'quit' to stop the agent.\n")


def show_help() -> None:
    """
    Display dynamic help based on tool schemas.
    """

    print("\nAvailable commands:\n")

    schemas = tool_registry.get_tool_schemas()

    for tool in schemas:

        name = tool["name"]

        properties = tool["input_schema"].get(
            "properties",
            {}
        )

        args = " ".join(properties.keys())

        print(f"  {name} {args}")

    print("\nExamples:")

    print("  read_file README.md")
    print("  list_directory .")
    print("  write_file test.txt hello")

    print("\nType 'exit' or 'quit' to stop the agent.\n")


def run_agent() -> None:
    """
    Interactive command loop for the search agent.
    """

    logger.info("Search agent started")

    logger.info(
        "Registered tools: %s",
        tool_registry.list_tools(),
    )

    show_startup_help()

    while True:

        try:
            query = input("\nSearch query: ")

        except KeyboardInterrupt:

            print("\nInterrupted")
            logger.info("Agent interrupted")
            break

        except EOFError:

            logger.info("Input closed")
            break

        query = query.strip()

        # -----------------------------
        # Help command
        # -----------------------------

        if query.lower() == "help":

            show_help()
            continue

        if not query:
            continue

        if query.lower() in ("exit", "quit"):

            logger.info("Agent exiting")
            break

        # -----------------------------
        # Parse command
        # -----------------------------

        parts = query.split()

        tool_name = parts[0]

        if tool_name == "write_file":

            if len(parts) < 3:

                print(
                    "Usage: write_file <path> <content>"
                )
                continue

            arguments = {
                "path": parts[1],
                "content": " ".join(parts[2:])
            }

        else:

            if len(parts) < 2:

                print(
                    f"Usage: {tool_name} <path>"
                )
                continue

            arguments = {
                "path": parts[1]
            }

        logger.info(
            "Executing tool: %s with args: %s",
            tool_name,
            arguments,
        )

        # -----------------------------
        # Execute tool
        # -----------------------------

        result = tool_registry.execute(
            tool_name,
            arguments,
        )

        # -----------------------------
        # Display result
        # -----------------------------

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    run_agent()