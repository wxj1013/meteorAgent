from typing import List, Dict, Any, Optional, Callable
import inspect
from llm import BaseLLM, DeepSeekLLM
import utils

# 角色，定义每个角色的工具和skill
class Role:
    _name: str = ""
    _tools = []
    # _skills: List[Skill] = []
    _llm_model: BaseLLM = None

    # 打包工具给大模型api
    @classmethod
    def pack_tools(cls) -> list:
        """生成 API 调用所需的 tools 参数（精简版）"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.doc or f"{tool.name} 工具",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            p.name: {
                                "type": utils.py_type_to_json(p.annotation),
                                "description": f"{p.name} 参数"
                            } for p in tool.parameters
                        },
                        "required": [
                            p.name for p in tool.parameters 
                            if p.default == inspect.Parameter.empty
                        ]
                    }
                }
            } for tool in cls._tools
        ]

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

    # 初始化llm模型，role继承时一定要调用。
    @classmethod
    def init_llm_model(cls, api_key: str, model: str, reasoning_effort: str, system_prompt: str):
        if "deepseek" in model:
            cls._llm_model = DeepSeekLLM(api_key, model, reasoning_effort, system_prompt)
        else:
            raise Exception(f"不支持当前模型:{model}")

    # 调用模型。在这里替换tools和skills
    @classmethod
    def chat(cls, message: str):
        system_prompt = cls._llm_model.system_prompt.format(tools = cls.tools_to_prompt())
        print(system_prompt)

        # return cls._llm_model.chat(message, system_prompt)
