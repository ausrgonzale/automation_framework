from pathlib import Path
from unittest.mock import Mock, patch

from ai.agents.testcase_generation_agent import (
    generate_testcases,
)
from ai.schemas.testcase_generation_request import (
    TestcaseGenerationRequest,
)


def test_generate_mock_testcase():

    # ------------------------------------------------------------------
    # Load mock AI response content
    # ------------------------------------------------------------------

    fixture_path = Path("tests/fixtures/mock_ai_response.json")

    mock_output_text = fixture_path.read_text()

    # ------------------------------------------------------------------
    # Patch AI client factory
    # ------------------------------------------------------------------

    with patch(
        "ai.agents.testcase_generation_agent.get_ai_client"
    ) as mock_client_factory:
        # Create mock client
        mock_client = Mock()
        # Patch the generate method to return the mock JSON string
        mock_client.generate.return_value = mock_output_text
        mock_client_factory.return_value = mock_client

        request = TestcaseGenerationRequest(
            story_id="AUTH-1",
            summary="User login",
            description="User can log in",
        )

        result = generate_testcases(request)

        # ------------------------------------------------------------------
        # Assertions
        # ------------------------------------------------------------------

        assert result is not None
        assert len(result.testcases) == 1

        # Optional stronger assertion (recommended)
        assert result.testcases[0].title is not None
