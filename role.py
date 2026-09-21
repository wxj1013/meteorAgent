from typing import List
import inspect
import json
from llm import DeepSeekLLM
import utils
from log import Logger
from utils import Task, mc

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
        self._llm_model = self._create_llm(api_key, model, reasoning_effort, self.__class__._system_prompt)

        # 每个role自己的代办任务清单
        self.tasks = {}

    # 每个实例持有独立的 LLM 客户端
    def _create_llm(self, api_key, model, reasoning_effort, system_prompt):
        if "deepseek" in model:
            return DeepSeekLLM(api_key, model, reasoning_effort, system_prompt)
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
    def _call_tool(self, tool_name: str, task: Task, **kwargs) -> str:
        for tool in self.__class__._tools:
            if tool.name == tool_name:
                try:
                    ret = tool.func(**kwargs)
                    # 子任务
                    if getattr(tool.func, 'subtask', False):
                        task.sub_tasks.append(ret)
                    return ret
                except Exception as e:
                    return f"调用工具错误：{e}"
        return f"角色「{self._name}」没有名为「{tool_name}」的工具"

    # 解决单任务
    def handle_task(self, task: Task):
        # 读取历史
        if task.historys:
            hist = task.historys
        else:
            hist = [{"role": "user", "content": task.content}]
            task.historys = hist

        tools = self._pack_tools()
        reported = False

        for iteration in range(self._max_iteration):
            assistant_msg = self._llm_model.chat(hist=hist, tools=tools)
            Logger.info(f"{self._name}-assistant: {assistant_msg.content}")

            # 没有工具调用时，视为任务完成，自动上报
            if not assistant_msg.tool_calls:
                if not reported:
                    mc.report_result(task.task_id, assistant_msg.content)
                    Logger.info(f"{self._name} 报告结果: {assistant_msg.content}")
                task.historys = []
                return

            # 保存 assistant 消息
            hist.append({
                "role": "assistant",
                "content": assistant_msg.content,
                "tool_calls": assistant_msg.tool_calls,
            })

            assistant_msg_content["tool_calls"] = assistant_msg.tool_calls
            hist.append(assistant_msg_content)

            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                Logger.info(f"{self._name}-tool-{tool_name}: {tool_call.id}")

                tool_result = self._call_tool(tool_name, task.task_id, **tool_args)
                hist.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

                Logger.info(f"{self._name}-tool-{tool_name}: {tool_result}")

                # 回报则结束
                if tool_name == "report_result":
                    reported = True
                    task.historys = []
                    return

            # 保存当前历史
            task.historys = hist

            # 如果有子任务，先把任务放到tasks
            if len(task.sub_tasks) > 0:
                self.tasks[task.task_id] = task
                return 

        mc.report_result(task.task_id, f"超过最大步数：{self._max_iteration}步，任务未完成。具体操作请查阅日志明细。")
        task.historys = []
        return

    # 检查子任务状态，将已完成的结果写入 task.historys
    def _update_subtasks(self, task: Task):
        if not task.historys:
            task.historys = [{"role": "user", "content": task.content}]

        completed = []
        for sub_id in task.sub_tasks:
            result = mc.fetch_result(sub_id)
            if result is not None:
                task.historys.append({
                    "role": "user",
                    "content": f"子任务 {sub_id} 的结果如下：\n{result}"
                })
                completed.append(sub_id)

        for sub_id in completed:
            task.sub_tasks.remove(sub_id)

    # 角色开始作业
    def run(self, poll_interval: float = 1.0):
        while True:
            # 处理等待子任务的任务
            for task_id, task in list(self.tasks.items()):
                self._update_subtasks(task)

                # 所有子任务已完成，继续原任务
                if len(task.sub_tasks) == 0:
                    self.tasks.pop(task_id, None)
                    Logger.info(f"{self._name} 继续任务: {task_id}")
                    self.handle_task(task)

            # 获取新任务
            new_task = mc.fetch_task(self.__class__._name)
            if new_task:
                Logger.info(f"{self._name} 收到新任务: {new_task.task_id}")
                self.handle_task(new_task)

            # 沉睡
            time.sleep(poll_interval)
