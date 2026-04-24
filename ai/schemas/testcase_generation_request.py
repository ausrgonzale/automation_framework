"""
Testcase Generation Request Schema

Purpose:
    Defines the input contract for generating testcases
    from a requirement such as a Jira story.

Architecture Role:
    Schema
"""

from pydantic import BaseModel


class CheckcaseGenerationRequest(BaseModel):
    """
    Input contract for testcase generation.
    """

    story_id: str
    summary: str
    description: str
