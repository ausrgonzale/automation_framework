from mcp.base.registry import MCPRegistry
from mcp.excel.excel_tool import ExcelTool
from mcp.tools.filesystem.append_file_tool import AppendFileTool
from mcp.tools.filesystem.directory_tool import ListDirectoryTool
from mcp.tools.filesystem.file_exists_tool import FileExistsTool
from mcp.tools.filesystem.read_file_tool import ReadFileTool
from mcp.tools.filesystem.search_text_tool import SearchTextTool
from mcp.tools.filesystem.search_tool import SearchFilesTool
from mcp.tools.filesystem.write_file_tool import WriteFileTool
from mcp.tools.jira.fetch_jira_tool import JiraFetchTool


def build_registry() -> MCPRegistry:
    """
    Build and return a fully initialized MCP registry.
    """

    registry = MCPRegistry()

    registry.register(ReadFileTool())
    registry.register(WriteFileTool())
    registry.register(AppendFileTool())
    registry.register(ListDirectoryTool())
    registry.register(SearchTextTool())
    registry.register(SearchFilesTool())
    registry.register(FileExistsTool())
    registry.register(ExcelTool())
    registry.register(JiraFetchTool())

    return registry
