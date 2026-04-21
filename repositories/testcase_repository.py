"""
===============================================================================
File: testcase_repository.py

Location:
    repositories/

Component Type:
    Repository Interface

Purpose:
    Defines the persistence contract for storing and retrieving test cases.

    This repository isolates the rest of the system from the underlying
    storage mechanism (filesystem, TestRail, database, etc.).

Architecture Role:
    Part of the Infrastructure / Persistence Layer.

    Agents and services interact with repositories instead of directly
    interacting with MCP tools or external storage systems.

System Context:

        TestCaseAgent
              ↓
        TestcaseGenerationService
              ↓
        TestcaseRepository
              ↓
        FileRepository / TestRailRepository / DatabaseRepository
              ↓
        MCP Tools / External APIs

Responsibilities:

    - Save generated test cases
    - Retrieve stored test cases
    - Check if test cases exist
    - List stored test cases

===============================================================================
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class TestcaseRepository(ABC):
        __test__ = False
    """
    Abstract base class defining the persistence contract
    for test case storage.
    """

    @abstractmethod
    def save(self, testcases: List[Dict[str, Any]]) -> None:
        """
        Persist generated test cases.
        """
        pass

    @abstractmethod
    def load(self, identifier: str) -> List[Dict[str, Any]]:
        """
        Retrieve stored test cases.
        """
        pass

    @abstractmethod
    def exists(self, identifier: str) -> bool:
        """
        Determine whether stored test cases exist.
        """
        pass

    @abstractmethod
    def list(self) -> List[str]:
        """
        List available stored test case identifiers.
        """
        pass