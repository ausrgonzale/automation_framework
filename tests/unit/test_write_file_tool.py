from pathlib import Path

from mcp.tools.filesystem.write_file_tool import WriteFileTool


def test_write_file_creates_file(tmp_path):

    tool = WriteFileTool()

    file_path = tmp_path / "test.txt"

    result = tool.execute(
        {
            "path": str(file_path),
            "content": "hello world",
        }
    )

    assert result["status"] == "success"

    assert file_path.exists()

    assert file_path.read_text() == "hello world"


def test_write_file_overwrites_existing_file(tmp_path):

    tool = WriteFileTool()

    file_path = tmp_path / "test.txt"

    file_path.write_text("old content")

    result = tool.execute(
        {
            "path": str(file_path),
            "content": "new content",
        }
    )

    assert result["status"] == "success"

    assert file_path.read_text() == "new content"