from tools.tool_registry import ToolRegistry
from tools.directory_tools import execute_list_directory, ListDirectoryArgs

def test_list_directory_returns_items(tmp_path):
    """
    Verify directory contents are listed.
    """

    # Create temporary files

    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("test")
    file2.write_text("test")

    args = ListDirectoryArgs(
        path=str(tmp_path)
    )

    result = execute_list_directory(args)

    assert "a.txt" in result
    assert "b.txt" in result

def test_list_directory_not_found():

    args = ListDirectoryArgs(
        path="does_not_exist_directory"
    )

    result = execute_list_directory(args)

    assert "Directory not found" in result

def test_list_directory_empty(tmp_path):
    """
    Verify empty directory message is returned.
    """

    args = ListDirectoryArgs(
        path=str(tmp_path)
    )

    result = execute_list_directory(args)

    assert result == "Directory is empty"