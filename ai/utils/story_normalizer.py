"""
Jira/Excel Story Normalizer Utility
- Accepts raw Jira or Excel user story dict
- Returns a normalized dict with consistent fields for prompt building
"""

from typing import Any, Dict


class StoryNormalizer:
    # Define the canonical field names for the framework

    CANONICAL_FIELDS = [
        "id",
        "summary",
        "description",
        "acceptance_criteria",
        "tool",
        "language",
        "priority",
        "related_to",
    ]

    @staticmethod
    def normalize(raw_story: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a Jira or Excel user story dict to a canonical format.
        Handles field mapping and extraction, including nested 'fields' dict for Jira.
        """
        field_map = {
            "id": ["id", "key", "story_id", "jira_id", "Story ID"],
            "summary": ["summary", "title", "name", "Summary"],
            "description": ["description", "details", "desc", "Description"],
            "acceptance_criteria": [
                "acceptance_criteria",
                "acceptanceCriteria",
                "criteria",
                "ac",
                "Acceptance Criteria",
            ],
            "tool": ["tool", "framework", "automation_tool", "Tool"],
            "language": ["language", "lang", "programming_language", "Language"],
            "priority": ["priority", "Priority"],
            "related_to": ["related_to", "Related"],
        }

        normalized = {}
        fields = raw_story.get("fields", {}) if isinstance(raw_story, dict) else {}
        for canonical, aliases in field_map.items():
            found = None
            for alias in aliases:
                # Prefer top-level, then nested 'fields'
                if alias in raw_story and raw_story[alias] is not None:
                    found = raw_story[alias]
                    break
                if alias in fields and fields[alias] is not None:
                    found = fields[alias]
                    break
            # Special handling for related_to: always as list
            if canonical == "related_to":
                if found is None:
                    normalized[canonical] = []
                elif isinstance(found, str):
                    # Support comma-separated string
                    if "," in found:
                        normalized[canonical] = [
                            s.strip() for s in found.split(",") if s.strip()
                        ]
                    else:
                        normalized[canonical] = [found]
                elif isinstance(found, list):
                    normalized[canonical] = found
                else:
                    normalized[canonical] = []
            else:
                normalized[canonical] = found if found is not None else ""

        # Always populate test_or_jira_id (prefer 'key', then 'id', then blank)
        normalized["test_or_jira_id"] = (
            raw_story.get("key") or raw_story.get("id") or fields.get("id") or ""
        )

        # Always populate related_to (as list, or blank)
        related_to = raw_story.get("related_to") or fields.get("related_to")
        if related_to is None:
            normalized["related_to"] = []
        elif isinstance(related_to, str):
            normalized["related_to"] = [related_to]
        elif isinstance(related_to, list):
            normalized["related_to"] = related_to
        else:
            normalized["related_to"] = []

        return normalized

    @staticmethod
    def to_prompt(story: Dict[str, Any]) -> str:
        """
        Build a compact prompt string from a normalized story dict.
        """
        prompt = f"Jira ID: {story['id']}\nSummary: {story['summary']}\nDescription: {story['description']}"
        if story.get("acceptance_criteria"):
            prompt += f"\nAcceptance Criteria: {story['acceptance_criteria']}"
        if story.get("tool"):
            prompt += f"\nTool: {story['tool']}"
        if story.get("language"):
            prompt += f"\nLanguage: {story['language']}"
        return prompt.strip()
