"""
===============================================================================
File: testcase_generation_service.py

Location:
    services/

Purpose:
    Provides workflow logic for generating test cases from requirements.

Design Principles:

    - Deterministic behavior
    - Clear separation of concerns
    - Repository-driven persistence
    - Fully testable
===============================================================================
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TestcaseGenerationService:
    __test__ = False
    """
    Service responsible for generating and validating test cases.
    """

    # ---------------------------------------------------------------------

    def __init__(
        self,
        repository: Any,  # Accepts CsvRepository or compatible
    ) -> None:
        """
        Initialize service with a repository.
        """
        self.repository = repository

    # ---------------------------------------------------------------------

    def generate_testcases(
        self,
        requirement: str,
        user_story_id: Optional[str] = None,
        extra_fields: Optional[dict] = None,
        testcase_index: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Generate and validate test cases from requirement text.
        Returns a list of testcases (not saved).
        """
        try:
            logger.info(
                "Generating test cases",
                extra={
                    "requirement_length": len(requirement),
                },
            )
            testcases = self._build_testcases(
                requirement,
                user_story_id=user_story_id,
                extra_fields=extra_fields or {},
                testcase_index=testcase_index,
            )
            self._validate_testcases(testcases)
            logger.info(
                "Test cases generated successfully",
                extra={
                    "count": len(testcases),
                },
            )
            return testcases
        except Exception:
            logger.exception("Test case generation failed")
            raise

    # ---------------------------------------------------------------------

    def _build_testcases(
        self,
        requirement: str,
        user_story_id: Optional[str] = None,
        extra_fields: Optional[dict] = None,
        testcase_index: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Build deterministic test cases for a single user story.
        """

        logger.debug("Building deterministic test cases")

        # Ensure extra_fields is always a dict
        if extra_fields is None:
            extra_fields = {}

        # Load Test ID config
        import json

        try:
            with open("templates/testcase_id_config.json") as f:
                id_config = json.load(f)
                prefix = id_config.get("prefix", "TC")
                start = int(id_config.get("start", 1))
        except Exception:
            prefix = "TC"
            start = 1

        # Generate unique Test ID (e.g., TC1, TC2, ...)
        test_id = f"{prefix}{start + testcase_index}"

        testcase = {
            "Test ID": test_id,
            "Title": extra_fields.get("summary", ""),
            "Steps": extra_fields.get("description", ""),
            "Expected Results": extra_fields.get("acceptance_criteria", ""),
            "Related To": (
                ",".join(extra_fields.get("related_to", []))
                if isinstance(extra_fields.get("related_to", []), list)
                else (extra_fields.get("related_to") or "")
            ),
            "Priority": extra_fields.get("priority", ""),
            "Language": extra_fields.get("language", ""),
            "Framework": extra_fields.get("tool", ""),
        }
        return [testcase]

    # ---------------------------------------------------------------------

    def _validate_testcases(
        self,
        testcases: List[Dict[str, Any]],
    ) -> None:
        """
        Validate test case structure for required fields.
        """

        logger.debug("Validating test cases")

        if not testcases:

            raise ValueError("No test cases generated")

        # Dynamically load required fields from the output template
        template_path = "templates/testcase_output_template.csv"
        try:
            with open(template_path, newline="") as f:
                import csv

                reader = csv.reader(f)
                required_fields = next(reader)
        except Exception:
            # Fallback to hardcoded columns if template missing
            required_fields = [
                "Test ID",
                "Title",
                "Steps",
                "Expected Results",
                "Related To",
                "Priority",
                "Language",
                "Framework",
            ]

        for testcase in testcases:

            for field in required_fields:

                if field not in testcase:

                    raise ValueError(f"Missing required field: {field}")
