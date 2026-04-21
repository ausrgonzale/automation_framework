from ai.prompts.testcase_generation import (
    build_testcase_generation_prompt,
)


def test_prompt_builder_returns_string():
    prompt = build_testcase_generation_prompt(
        jira_story="User can reset password"
    )

    assert isinstance(prompt, str)
    assert "Schema:" in prompt
    assert "Jira Story:" in prompt