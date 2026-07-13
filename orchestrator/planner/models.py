from pydantic import BaseModel, Field
from typing import Literal, Dict, Any

class Action(BaseModel):
    thought: str = Field(description="为什么这么做")
    tool: Literal["read_file", "write_file", "run_shell", "finish"] = Field()
    args: Dict[str, Any] = Field(default_factory=dict)