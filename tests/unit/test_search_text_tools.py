from mcp.tools.filesystem.search_text_tool import SearchTextTool


def test_search_text_finds_matches(tmp_path):

    tool = SearchTextTool()

    file_path = tmp_path / "file.txt"

    file_path.write_text(
        "hello world\n"
        "another line\n"
        "hello again"
    )

    result = tool.execute(
        {
            "path": str(file_path),
            "text": "hello",
        }
    )

    assert result["status"] == "success"

    assert result["count"] == 2

    assert result["matches"][0]["line_number"] == 1


def test_search_text_no_matches(tmp_path):

    tool = SearchTextTool()

    file_path = tmp_path / "file.txt"

    file_path.write_text("nothing here")

    result = tool.execute(
        {
            "path": str(file_path),
            "text": "missing",
        }
    )

    assert result["status"] == "success"

    assert result["count"] == 0