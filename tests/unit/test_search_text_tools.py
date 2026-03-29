from tools.search_text_tools import (
    execute_search_text,
    SearchTextArgs,
)


def test_search_text_success(tmp_path):

    file_path = tmp_path / "test.txt"

    file_path.write_text(
        "hello\nerror occurred\nbye"
    )

    args = SearchTextArgs(
        path=str(file_path),
        pattern="error",
    )

    result = execute_search_text(args)

    assert "error occurred" in result


def test_search_text_no_match(tmp_path):

    file_path = tmp_path / "test.txt"

    file_path.write_text("hello")

    args = SearchTextArgs(
        path=str(file_path),
        pattern="error",
    )

    result = execute_search_text(args)

    assert result == "No matches found"


def test_search_text_path_not_found():

    args = SearchTextArgs(
        path="does_not_exist",
        pattern="error",
    )

    result = execute_search_text(args)

    assert "Path not found" in result