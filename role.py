from typing import List, Dict, Any, Optional, Callable
import inspect
from llm import BaseLLM, DeepSeekLLM
import utils
import json
from log import Logger

# 角色，定义每个角色的工具和skill
class Role:
    _name: str = ""
    _tools = []
    # _skills: List[Skill] = []
    _llm_model: BaseLLM = None
    _max_iteration: 10
    _max_retry: 3

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

    # 解决单任务
    @classmethod
    def handle_task(cls, task: str) -> str:
        tools = cls.pack_tools()
        hist = [{
            "role": "user", 
            "content": task
        }]
        iteration = 0

        Logger.info(cls._name + "-user:" + task)

        while iteration < cls._max_iteration:
            assistant_msg = cls._llm_model.chat(hist = hist, tools = tools)

            assistant_msg_content = {
                "role": "assistant", 
                "content": assistant_msg.content
            }

            Logger.info(cls._name + "-assistant:" + assistant_msg.content)

            if not assistant_msg.tool_calls:
                return assistant_msg.content

            assistant_msg_content["tool_calls"] = assistant_msg.tool_calls
            hist.append(assistant_msg_content)

            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                Logger.info(cls._name + "-tool-" + tool_name + ":" + tool_call.id)

                tool_result = cls.call_tool(tool_name, **tool_args)
                hist.append({
                    "role": "tool", 
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

                Logger.info(cls._name + "-tool-" + tool_name + ":" + tool_result)

            iteration += 1

        return f"超过最大步数：{cls._max_iteration}步，任务未完成。当前进度{assistant_msg.content}"

