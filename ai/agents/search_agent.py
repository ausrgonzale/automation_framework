import logging

from config.logging_config import configure_logging
from mcp.base.registry import MCPRegistry


class SearchAgent:
    def __init__(self, tool_registry: MCPRegistry):
        configure_logging()
        self.logger = logging.getLogger(__name__)
        self.tool_registry = tool_registry

    def show_startup_help(self) -> None:
        print("\nSearch Agent started\n")
        tools = self.tool_registry.list_tools()
        print("Available commands:\n")
        for tool in tools:
            print(f"  {tool} <path>")
            print(f"      Example: {tool} README.md\n")
        print("Type 'help' to see this list again.")
        print("Type 'exit' or 'quit' to stop the agent.\n")

    def show_help(self) -> None:
        print("\nAvailable commands:\n")
        # Synthesize help from registered tools
        for tool_name in self.tool_registry.list_tools():
            # Guess argument pattern by tool name
            if tool_name in ("write_file", "append_file"):
                args = "path content"
            elif tool_name == "search_text":
                args = "path pattern"
            else:
                args = "path"
            print(f"  {tool_name} {args}")
        print("\nExamples:")
        print("  read_file README.md")
        print("  list_directory .")
        print("  write_file test.txt hello")
        print("\nType 'exit' or 'quit' to stop the agent.\n")

    def run(self) -> None:
        self.logger.info("Search agent started")
        self.logger.info("Registered tools: %s", self.tool_registry.list_tools())
        self.show_startup_help()
        while True:
            try:
                query = input("\nSearch query: ")
            except KeyboardInterrupt:
                print("\nInterrupted")
                self.logger.info("Agent interrupted")
                break
            except EOFError:
                self.logger.info("Input closed")
                break
            query = query.strip()
            if query.lower() == "help":
                self.show_help()
                continue
            if not query:
                continue
            if query.lower() in ("exit", "quit"):
                self.logger.info("Agent exiting")
                break
            parts = query.split()
            tool_name = parts[0]
            if tool_name in ("write_file", "append_file"):
                if len(parts) < 3:
                    print(f"Usage: {tool_name} <path> <content>")
                    continue
                arguments = {"path": parts[1], "content": " ".join(parts[2:])}
            elif tool_name == "search_text":
                if len(parts) < 3:
                    print("Usage: search_text <path> <pattern>")
                    continue
                arguments = {"path": parts[1], "pattern": " ".join(parts[2:])}
            else:
                if len(parts) < 2:
                    print(f"Usage: {tool_name} <path>")
                    continue
                arguments = {"path": parts[1]}
            self.logger.info("Executing tool: %s with args: %s", tool_name, arguments)
            tool = None
            if hasattr(self.tool_registry, "get_tool"):
                try:
                    tool = self.tool_registry.get_tool(tool_name)
                except Exception as e:
                    print(f"Error: {e}")
            if tool and hasattr(tool, "execute"):
                result = tool.execute(arguments)
            else:
                result = {
                    "status": "error",
                    "message": f"Tool '{tool_name}' not found or not executable.",
                }
            print("\nResult:")
            print(result)


# Example usage if running as script
if __name__ == "__main__":
    from mcp.registry_setup import build_registry

    agent = SearchAgent(build_registry())
    agent.run()
