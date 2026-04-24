"""
===============================================================================
File: file_repository.py

Location:
    repositories/

Component Type:
    Repository Implementation

Purpose:
    Provides filesystem-based persistence for generated test cases.

    This repository implementation stores test cases as JSON files using
    the MCP filesystem tools. It serves as the default persistence mechanism
    for the automation framework during early development.

Architecture Role:
    Concrete implementation of the TestcaseRepository interface.

    This repository translates repository operations into filesystem actions
    executed through MCP tools. It ensures that higher-level components
    remain independent of storage details.

System Context:

        TestCaseAgent
              ↓
        TestcaseGenerationService
              ↓
        FileRepository
              ↓
        write_file_tool / read_file_tool / file_exists_tool
              ↓
        Filesystem

Responsibilities:

    - Save test cases to disk
    - Load test cases from disk
    - Check existence of stored test cases
    - List stored test case files

Storage Strategy:

    Test cases are stored as JSON files in the configured storage directory.

    Example:

        storage/
            login_tests.json
            registration_tests.json

Design Principles:

    - Deterministic behavior
    - Storage abstraction
    - Tool-based filesystem access
    - Replaceable persistence layer

===============================================================================
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from mcp.tools.filesystem.file_exists_tool import FileExistsTool
from mcp.tools.filesystem.read_file_tool import ReadFileTool
from mcp.tools.filesystem.write_file_tool import WriteFileTool
from repositories.testcase_repository import CheckcaseRepository

logger = logging.getLogger(__name__)


class FileRepository(CheckcaseRepository):
    """
    Filesystem-based implementation of the TestcaseRepository.
    """

    def __init__(self, storage_directory: str = "storage"):
        """
        Initialize repository.

        Parameters:

            storage_directory:
                Directory where test cases will be stored.
        """

        self.storage_directory = Path(storage_directory)

        # Ensure directory exists

        self.storage_directory.mkdir(parents=True, exist_ok=True)

        # MCP tools

        self.write_tool = WriteFileTool()
        self.read_tool = ReadFileTool()
        self.exists_tool = FileExistsTool()

    # ---------------------------------------------------------------------

    def _build_path(self, identifier: str) -> Path:
        """
        Build the full file path for a test case set.
        """

        filename = f"{identifier}.json"

        return self.storage_directory / filename

    # ---------------------------------------------------------------------

    def save(self, testcases: List[Dict[str, Any]]) -> None:
        """
        Persist test cases to disk.
        """

        if not testcases:
            raise ValueError("testcases list cannot be empty")

        identifier = testcases[0].get("identifier", "testcases")

        path = self._build_path(identifier)

        logger.info(
            "Saving test cases",
            extra={
                "identifier": identifier,
                "path": str(path),
            },
        )

        payload = json.dumps(testcases, indent=2)

        self.write_tool.execute(
            arguments={
                "path": str(path),
                "content": payload,
            }
        )

    # ---------------------------------------------------------------------

    def load(self, identifier: str) -> List[Dict[str, Any]]:
        """
        Retrieve stored test cases.
        """

        path = self._build_path(identifier)

        logger.info(
            "Loading test cases",
            extra={
                "identifier": identifier,
                "path": str(path),
            },
        )

        result = self.read_tool.execute(
            arguments={
                "path": str(path),
            }
        )

        content = result["content"]

        return json.loads(content)

    # ---------------------------------------------------------------------

    def exists(self, identifier: str) -> bool:
        """
        Determine whether stored test cases exist.
        """

        path = self._build_path(identifier)

        result = self.exists_tool.execute(
            arguments={
                "path": str(path),
            }
        )

        return result["exists"]

    # ---------------------------------------------------------------------

    def list(self) -> List[str]:
        """
        List available stored test case identifiers.
        """

        logger.info(
            "Listing stored test cases",
            extra={
                "directory": str(self.storage_directory),
            },
        )

        files = self.storage_directory.glob("*.json")

        return [file.stem for file in files]
