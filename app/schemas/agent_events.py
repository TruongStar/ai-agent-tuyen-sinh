from pydantic import BaseModel
from typing import Any, Literal

class AgentEvent(BaseModel):
    type: Literal["thinking", "tool_start", "tool_result", "message", "final", "error"]
    content: str = ""
    tool_name: str | None = None
    args: dict[str, Any] | None = None
