from typing import List, Dict, Any, Optional, Callable
from tools import Tool
import inspect

# 角色，定义每个角色的工具和skill
class Role:
    def __init__(self, name: str):
        self.name = name
        self.tools: List[Tool] = []
        # self.skills: List[Skill] = []

    # 新增一个工具
    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    # 把工具输出为prompt
    def tools_to_prompt(self) -> str:
        if not self.tools:
            return f"角色「{self.name}」目前没有可用工具。"
        
        lines = [f"角色「{self.name}」可使用的工具有："]
        for idx, tool in enumerate(self.tools, start=1):
            lines.append(f"\n--- 工具 {idx} ---")
            lines.append(tool.to_natural_language())
        return "\n".join(lines)

    # 调用一个工具
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.func(**kwargs)
        raise ValueError(f"角色「{self.name}」没有名为「{tool_name}」的工具")

    def __repr__(self):
        return f"Role('{self.name}', tools={[t.name for t in self.tools]})"

# 工具注册函数，标注一个工具能被哪些角色所用
def assign_to(*roles: Role):
    def decorator(func: Callable) -> Callable:
        # 通过inspect获取函数的入参、出参、docstring
        sig = inspect.signature(Callable)
        # 构建 Tool 对象
        tool = Tool(
            name=func.__name__,
            func=func,
            parameters=sig.parameters.items(),
            returns=sig.return_annotation,
            description=Callable.__doc__
        )
        for role in roles:
            role.add_tool(tool)
        return func  # 原函数不变，仍可独立调用
    return decorator