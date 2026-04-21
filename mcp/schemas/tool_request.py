from typing import Any, Dict

from pydantic import BaseModel


class ToolRequest(BaseModel):

    tool_name: str
    arguments: Dict[str, Any]