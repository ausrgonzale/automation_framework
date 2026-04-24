import os

import pytest

from ai.agents.testcase_generation_agent import (
    generate_testcases,
)
from ai.schemas.testcase_generation_request import (
    CheckcaseGenerationRequest,
)

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "true",
    reason="Integration tests disabled",
)


@pytest.mark.integration
def test_generate_ai_testcase():

    story = """
    User can log in using valid credentials.
    """

    request = CheckcaseGenerationRequest(
        story_id="AUTH-1",
        summary="User Login",
        description=story,
    )

    result = generate_testcases(request)

    assert len(result.testcases) > 0
