from typing import List, Dict, Any, Optional, Callable
import inspect
from llm import BaseLLM, DeepSeekLLM

# 角色，定义每个角色的工具和skill
class Role:
    _name: str = ""
    _tools = []
    # _skills: List[Skill] = []
    _llm_model: BaseLLM = None

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
    def call_tool(cls, tool_name: str, **kwargs) -> str:
        for tool in cls._tools:
            if tool.name == tool_name:
                try:
                    return tool.func(**kwargs)
                except Exception as e:
                    return f"调用工具错误：{e}"

        return f"角色「{cls._name}」没有名为「{tool_name}」的工具"

    # 初始化llm模型
    @classmethod
    def init_llm_model(cls, api_key: str, model: str, reasoning_effort: str, system_prompt: str):
        if "deepseek" in model:
            cls._llm_model = DeepSeekLLM(api_key, model, reasoning_effort, system_prompt)
        else:
            raise Exception(f"不支持当前模型:{model}")
