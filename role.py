from typing import List
import inspect
import json
from llm import DeepSeekLLM
import utils
from log import Logger
from utils import Task

# 角色，定义每个角色的工具和skill
class Role:
    _name: str = ""
    _tools: List = []
    # _skills: List[Skill] = []
    _max_iteration: int = 10
    _max_retry: int = 3
    _system_prompt: str = ""

    def __init__(
        self,
        api_key: str,
        model: str = "",
        reasoning_effort: str = "",
        max_iteration: int = None,
        max_retry: int = None,
        name: str = None,
    ):
        # 名称：允许实例覆盖，默认取子类 _name
        self._name = name or self.__class__._name

        # 运行参数：允许实例覆盖，否则取类默认值
        if max_iteration is not None:
            self._max_iteration = max_iteration
        if max_retry is not None:
            self._max_retry = max_retry

        # LLM 客户端
        if "deepseek" in model:
        self._llm_model = self._create_llm(api_key, model, reasoning_effort, self.__class__._system_prompt)

        # 每个role自己的代办任务清单
        self.tasks = {}

    # 每个实例持有独立的 LLM 客户端
    def _create_llm(self, api_key, model, reasoning_effort, system_prompt):
        if "deepseek" in model:
            return DeepSeekLLM(api_key, model, reasoning_effort, system_prompt,)
        raise Exception(f"不支持当前模型:{model}")


    # 打包工具给大模型api
    def _pack_tools(self) -> list:
        """生成 API 调用所需的 tools 参数（只读取共享的 _tools，安全）"""
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
                                "description": f"{p.name} 参数",
                            }
                            for p in tool.parameters
                        },
                        "required": [
                            p.name
                            for p in tool.parameters
                            if p.default == inspect.Parameter.empty
                        ],
                    },
                },
            }
            for tool in self.__class__._tools  # 明确从类读取
        ]

    # 调用一个工具
    def _call_tool(self, tool_name: str, **kwargs) -> str:
        for tool in self.__class__._tools:
            if tool.name == tool_name:
                try:
                    return tool.func(**kwargs)
                except Exception as e:
                    return f"调用工具错误：{e}"
        return f"角色「{self._name}」没有名为「{tool_name}」的工具"

    # 解决单任务
    def handle_task(cls, task: str) -> str:
        tools = cls.pack_tools()
        hist = [{"role": "user", "content": task}]
        iteration = 0

        Logger.info(f"{self._name}-user: {task}")

        while iteration < self._max_iteration:   # 实例属性或类属性均可安全读取
            assistant_msg = self._llm_model.chat(hist=hist, tools=tools)

            assistant_msg_content = {
                "role": "assistant",
                "content": assistant_msg.content,
            }

            Logger.info(f"{self._name}-assistant: {assistant_msg.content}")

            if not assistant_msg.tool_calls:
                self._memory.append({"task": task, "result": assistant_msg.content})
                return assistant_msg.content

            assistant_msg_content["tool_calls"] = assistant_msg.tool_calls
            hist.append(assistant_msg_content)

            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                Logger.info(f"{self._name}-tool-{tool_name}: {tool_call.id}")

                tool_result = self._call_tool(tool_name, **tool_args)
                hist.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

                Logger.info(f"{self._name}-tool-{tool_name}: {tool_result}")

            iteration += 1

            # 如果有代办任务，先把任务放到tasks

        return f"超过最大步数：{self._max_iteration}步，任务未完成。具体操作请查阅日志明细。"
