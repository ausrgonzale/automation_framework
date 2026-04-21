import logging
from typing import Any, Dict

from mcp.base.tool import MCPTool

logger = logging.getLogger(__name__)


class JiraFetchTool(MCPTool):
    name = "fetch_jira_stories"

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        arguments: {"jira_ids": str}
        jira_ids: comma or tab separated string of Jira IDs
        """
        jira_ids = arguments.get("jira_ids", "")
        ids = [i.strip() for i in jira_ids.replace("\t", ",").split(",") if i.strip()]
        if not ids:
            return {"status": "error", "message": "No Jira IDs provided."}
        # Placeholder: Replace with real Jira API integration
        stories = []
        for jid in ids:
            # Simulate fetching from Jira
            stories.append(
                {
                    "id": jid,
                    "summary": f"Summary for {jid}",
                    "description": f"Description for {jid}",
                    "acceptance_criteria": f"Acceptance criteria for {jid}",
                    # Optionally: tool/language fields
                }
            )
        logger.info(f"Fetched {len(stories)} stories from Jira: {ids}")
        return {"status": "success", "stories": stories}
