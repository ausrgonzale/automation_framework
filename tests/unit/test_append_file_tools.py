from mcp.tools.filesystem.append_file_tool import AppendFileTool


def test_append_file_adds_content(tmp_path):

    tool = AppendFileTool()

    file_path = tmp_path / "test.txt"

    result = tool.execute(
        {
            "path": str(file_path),
            "content": "first line",
        }
    )

    assert result["status"] == "success"

    result = tool.execute(
        {
            "path": str(file_path),
            "content": "second line",
        }
    )

    assert result["status"] == "success"

    content = file_path.read_text()

    assert "first line" in content

    assert "second line" in content


def test_append_file_creates_file_if_missing(tmp_path):

    tool = AppendFileTool()

    file_path = tmp_path / "new_file.txt"

    result = tool.execute(
        {
            "path": str(file_path),
            "content": "content",
        }
    )

    assert result["status"] == "success"

    assert file_path.exists()