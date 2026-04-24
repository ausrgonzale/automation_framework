"""
Coding Agent

Purpose:
    Provides an interactive AI-driven development assistant capable of
    reading, writing, editing files, and executing shell commands using
    tool-based workflows.

Responsibilities:
    - Accept user requests via an interactive loop
    - Use AI to determine required actions
    - Invoke filesystem and system tools (read, write, edit, bash)
    - Maintain conversational context across steps
    - Handle tool execution and return results to the model

Scope:
    This agent is a general-purpose development and code manipulation
    assistant. It is not responsible for orchestration or domain-specific
    workflows such as test generation or test execution.

Architecture Role:
    Sub-Agent (Worker)

    The Coding Agent operates under the control of an Orchestration Agent.
    It performs task execution using tools (MCPs) but does not route or
    coordinate workflows.

Dependencies:
    - AI client factory (provider-agnostic)
    - Tool execution functions
    - Filesystem access
    - Shell command execution

Future Evolution:
    This agent may be invoked by the Orchestration Agent to perform
    development, debugging, or code modification tasks within automated
    workflows.

Example Use Cases:
    - Refactor code
    - Fix failing tests
    - Generate files
    - Run shell commands
    - Inspect project structure
"""

import logging

from ai.client_factory import get_ai_client
from ai.prompts.testcase_generation import (
    build_testcase_generation_prompt,
)
from ai.schemas.testcase import CheckCaseSet
from ai.schemas.testcase_generation_request import (
    CheckcaseGenerationRequest,
)

logger = logging.getLogger(__name__)


def generate_testcases(
    request: CheckcaseGenerationRequest,
) -> CheckCaseSet:
    """
    Generate structured testcases from a validated request.
    """

    logger.info(
        "Generating testcases",
        extra={"story_id": request.story_id},
    )

    client = get_ai_client()

    prompt = build_testcase_generation_prompt(jira_story=request.description)

    response_text = client.generate(
        prompt=prompt,
        temperature=0.0,
        max_tokens=300,
    )

    try:
        testcases = CheckCaseSet.model_validate_json(response_text)
    except Exception:
        logger.error(
            "Failed to parse AI response",
            extra={
                "story_id": request.story_id,
                "response": response_text,
            },
            exc_info=True,
        )

        raise
    logger.info(
        "Generated %s testcases",
        len(testcases.testcases),
    )

    return testcases
