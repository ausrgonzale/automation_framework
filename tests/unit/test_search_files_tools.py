from mcp.tools.filesystem.search_tool import SearchFilesTool


def test_search_files_finds_matching_files(tmp_path):

    tool = SearchFilesTool()

    (tmp_path / "a.txt").write_text("a")

    (tmp_path / "b.log").write_text("b")

    result = tool.execute(
        {
            "path": str(tmp_path),
            "pattern": "*.txt",
        }
    )

    assert result["status"] == "success"

    assert result["count"] == 1

    assert any("a.txt" in match for match in result["matches"])


def test_search_files_path_not_found():

    tool = SearchFilesTool()

    result = tool.execute(
        {
            "path": "does_not_exist",
            "pattern": "*.txt",
        }
    )

    assert result["status"] == "error"