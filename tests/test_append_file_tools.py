from tools.append_file_tools import (
    execute_append_file,
    AppendFileArgs,
)

def test_append_file_success(tmp_path):
    """
    Verify content is appended to a new file.
    """

    file_path = tmp_path / "test.txt"

    args = AppendFileArgs(
        path=str(file_path),
        content="hello",
    )

    result = execute_append_file(args)

    assert "Content appended" in result

    assert file_path.exists()

    assert file_path.read_text() == "hello\n"


def test_append_file_multiple_appends(tmp_path):
    """
    Verify multiple appends add lines correctly.
    """

    file_path = tmp_path / "test.txt"

    execute_append_file(
        AppendFileArgs(
            path=str(file_path),
            content="first",
        )
    )

    execute_append_file(
        AppendFileArgs(
            path=str(file_path),
            content="second",
        )
    )

    assert file_path.read_text() == (
        "first\nsecond\n"
    )


def test_append_file_creates_parent_directory(tmp_path):
    """
    Verify missing directories are created automatically.
    """

    nested_file = tmp_path / "logs" / "output.txt"

    args = AppendFileArgs(
        path=str(nested_file),
        content="data",
    )

    execute_append_file(args)

    assert nested_file.exists()

    assert nested_file.read_text() == "data\n"


def test_append_file_invalid_path():
    """
    Verify error is returned for invalid path.
    """

    args = AppendFileArgs(
        path="/invalid/path/test.txt",
        content="data",
    )

    result = execute_append_file(args)

    assert "File append error" in result