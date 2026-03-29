from pathlib import Path

from tools.write_file_tools import (
    execute_write_file,
    WriteFileArgs,
)


def test_write_file_success(tmp_path):
    """
    Verify file is created and content written.
    """

    file_path = tmp_path / "test.txt"

    args = WriteFileArgs(
        path=str(file_path),
        content="hello",
    )

    result = execute_write_file(args)

    assert "File written" in result

    assert file_path.exists()

    assert file_path.read_text() == "hello"


def test_write_file_overwrite(tmp_path):
    """
    Verify existing file content is overwritten.
    """

    file_path = tmp_path / "test.txt"

    file_path.write_text("old")

    args = WriteFileArgs(
        path=str(file_path),
        content="new",
    )

    execute_write_file(args)

    assert file_path.read_text() == "new"


def test_write_file_invalid_path():
    """
    Verify error is returned for invalid path.
    """

    args = WriteFileArgs(
        path="/invalid/path/test.txt",
        content="data",
    )

    result = execute_write_file(args)

    assert "File write error" in result