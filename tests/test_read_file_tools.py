from tools.file_tools import execute_read_file, ReadFileArgs


def test_read_file_success(tmp_path):
    """
    Verify file contents are returned.
    """

    file_path = tmp_path / "test.txt"

    file_path.write_text("hello")

    args = ReadFileArgs(
        path=str(file_path)
    )

    result = execute_read_file(args)

    assert result == "hello"

def test_read_file_not_found():

    args = ReadFileArgs(
        path="does_not_exist.txt"
    )

    result = execute_read_file(args)

    assert "File read error" in result

def test_read_file_empty_file(tmp_path):
    """
    Verify empty file returns empty string.
    """

    file_path = tmp_path / "empty.txt"

    file_path.write_text("")

    args = ReadFileArgs(
        path=str(file_path)
    )

    result = execute_read_file(args)

    assert result == ""