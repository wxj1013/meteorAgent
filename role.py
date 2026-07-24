from typing import List, Dict, Any, Optional, Callable
from tools import Tool
import inspect

# 角色，定义每个角色的工具和skill
class Role:
    _name: str = ""
    _tools: List[Tool] = []
    # _skills: List[Skill] = []

    # 把工具输出为prompt
    @classmethod
    def tools_to_prompt(cls) -> str:
        if not cls._tools:
            return f"角色「{cls._name}」没有可用工具。"
        
        lines = [f"角色「{cls._name}」可使用的工具有："]
        for idx, tool in enumerate(_tools, start=1):
            lines.append(f"\n--- 工具 {idx} ---")
            lines.append(tool.to_natural_language())
        return "\n".join(lines)

    # 调用一个工具
    @classmethod
    def call_tool(cls, tool_name: str, **kwargs) -> Any:
        for tool in cls._tools:
            if tool.name == tool_name:
                try:
                    return tool.func(**kwargs)
                except Exception as e:
                    return f"调用工具错误：{e}"

        raise ValueError(f"角色「{cls._name}」没有名为「{tool_name}」的工具")

# 注册工具权限，注册后可以通过call_tool来使用。
def assign_to(*role_classes: type):
    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)
        tool = Tool(
            func=func,
            parameters=list(sig.parameters.values()), 
            returns=sig.return_annotation,
            description=func.__doc__
        )
        for role_cls in role_classes:
            role_cls._tools.append(tool)
        return func
    return decorator