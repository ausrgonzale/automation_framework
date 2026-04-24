import json

from ai.schemas.testcase import CheckCaseSet


def build_testcase_generation_prompt(
    jira_story: str,
) -> str:
    """
    Build a prompt instructing the AI to generate
    structured test cases that match the TestCaseSet schema.

    This ensures deterministic, machine-parseable output.
    """

    schema_json = json.dumps(
        CheckCaseSet.model_json_schema(),
        indent=2,
    )

    prompt = f"""
You are a senior QA automation engineer.

Generate comprehensive test cases for the Jira story below.

Return ONLY valid JSON.
Do not include explanations, markdown, or commentary.
Your response must conform exactly to the schema provided.

Schema:
{schema_json}

Jira Story:
{jira_story}
"""

    return prompt.strip()
