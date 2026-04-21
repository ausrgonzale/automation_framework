from mcp.tools.filesystem.directory_tool import ListDirectoryTool


def test_list_directory_returns_files(tmp_path):

    tool = ListDirectoryTool()

    (tmp_path / "a.txt").write_text("a")

    (tmp_path / "b.txt").write_text("b")

    result = tool.execute(
        {
            "path": str(tmp_path),
        }
    )

    assert result["status"] == "success"

    assert result["count"] == 2

    assert "a.txt" in result["items"]

    assert "b.txt" in result["items"]


def test_list_directory_empty(tmp_path):

    tool = ListDirectoryTool()

    result = tool.execute(
        {
            "path": str(tmp_path),
        }
    )

    assert result["status"] == "success"

    assert result["count"] == 0