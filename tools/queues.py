from utils import mc
import time
from utils import Task
from .tool import assign_to
from coder import Coder

@assign_to(Coder)
def assign_task(target: str, content: str) -> str:
    """
    通过消息队列，发布任务给planner以外的其他角色。
    coder: 编码者，负责写代码
    analyst：数据分析师，负责数据处理和加工
    engineer：模型工程师，负责模型相关工作
    tester：测试，负责测试和报告编写

    Args:
        target (str): 要发布任务的对象，可选项：coder, analyst, engineer, tester
        content (str): 发布的任务具体内容

    Returns:
        str: 任务编号。任务完成后会返回任务完成描述。如果发布失败，会返回失败信息
    """
    if target not in ["coder", "analyst", "engineer", "tester"]:
        return "target参数错误，支持coder, analyst, engineer, tester。请确认任务的发布对象后重填"
    task_id = mc.publish_task(target, content)
    return task_id

@assign_to(Coder)
def report_result(result: str, task_id: str = None) -> str:
    """
    把任务完成的信息反馈给消息队列。调用此方法后，任务会结束。

    Args:
        result (str): 回报任务完成的信息与总结。
        task_id (str): 要回报的任务编号，不要传，回报时会自动找到正确的任务编号。

    Returns:
        str: 任务回报成功（成功），或描述错误的字符串（失败）。
    """
    try:
        mc.report_result(task_id, result)
        return f"任务：{task_id}，任务结果回报成功"
    except Exception as e:
        return f"任务回报失败：{str(e)}，建议立即回报用户，检查任务队列配置情况。"