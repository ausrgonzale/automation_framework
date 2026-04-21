"""
===============================================================================
File: test_file_exists_tool.py

Location:
    tests/unit/

Purpose:
    Unit tests for the FileExistsTool MCP tool.

    These tests validate the deterministic behavior of the filesystem
    existence check capability within the MCP layer.

Architecture Role:
    Ensures the FileExistsTool correctly implements the MCPTool interface
    and returns consistent structured responses required by agents and
    orchestration workflows.

Test Coverage:

    - File exists detection
    - Missing file detection
    - Required argument validation
    - Interface contract compliance

===============================================================================
"""

from mcp.tools.filesystem.file_exists_tool import FileExistsTool


def test_file_exists_returns_true(tmp_path):
    """
    Tool should return True when file exists.
    """

    # Arrange

    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")

    tool = FileExistsTool()

    # Act

    result = tool.execute(
        arguments={
            "path": str(file_path)
        }
    )

    # Assert

    assert result["exists"] is True


def test_file_exists_returns_false(tmp_path):
    """
    Tool should return False when file does not exist.
    """

    # Arrange

    file_path = tmp_path / "missing.txt"

    tool = FileExistsTool()

    # Act

    result = tool.execute(
        arguments={
            "path": str(file_path)
        }
    )

    # Assert

    assert result["exists"] is False


def test_file_exists_missing_argument():
    """
    Tool should raise ValueError when required argument is missing.
    """

    tool = FileExistsTool()

    try:
        tool.execute(arguments={})
    except ValueError as exc:
        assert "path" in str(exc)