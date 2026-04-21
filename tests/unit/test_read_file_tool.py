from mcp.tools.filesystem.read_file_tool import ReadFileTool


def test_read_file_success(tmp_path):
    """
    Verify file contents are returned.
    """

    tool = ReadFileTool()

    file_path = tmp_path / "test.txt"

    file_path.write_text("hello")

    result = tool.execute(
        {
            "path": str(file_path)
        }
    )

    assert result["status"] == "success"

    assert result["content"] == "hello"


def test_read_file_not_found():

    tool = ReadFileTool()

    result = tool.execute(
        {
            "path": "does_not_exist.txt"
        }
    )

    assert result["status"] == "error"

    assert "No such file" in result["message"]


def test_read_file_empty_file(tmp_path):
    """
    Verify empty file returns empty string.
    """

    tool = ReadFileTool()

    file_path = tmp_path / "empty.txt"

    file_path.write_text("")

    result = tool.execute(
        {
            "path": str(file_path)
        }
    )

    assert result["status"] == "success"

    assert result["content"] == ""