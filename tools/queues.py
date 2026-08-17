import uuid
from queue import Queue
from coder import Coder
from planner import Planner

# 全局队列
queue_planner: Queue = Queue()
queue_coder: Queue = Queue()


@assign_to(Coder)
def task_finish(task_id: str, finish_msg: str) -> str:
    """
    向 Planner 回报任务执行结果。

    由 Coder 在执行完一个任务后调用，将任务 ID 和执行结果放入结果队列（queue_planner），
    供 Planner 后续取用。框架会自动将参数打包成合适格式。

    Args:
        task_id (str): 任务的唯一标识符，由 Planner 在发布任务时生成。
        finish_msg (str): 任务执行的最终结果或状态描述（如成功、失败原因、输出等）。

    Returns:
        str: 回报成功的确认消息，包含 task_id，例如 "任务 {task_id} 已回报"；
             若发生内部错误，返回描述错误的字符串。
    """
    try:
        # 直接将 task_id 和 finish_msg 放入队列（框架会打包）
        queue_planner.put((task_id, finish_msg))
        return f"任务 {task_id} 已回报"
    except Exception as e:
        return f"错误：回报任务 {task_id} 时发生异常: {e}"


@assign_to(Planner)
def task_coder(task_msg: str, timeout: Optional[float] = None) -> str:
    """
    向 Coder 发布一个新任务，并返回任务 ID。

    由 Planner 调用，自动生成全局唯一的 task_id，将任务消息放入任务队列（queue_coder）。
    Coder 会从该队列中获取任务并执行。

    Args:
        task_msg (str): 要发送给 Coder 的任务描述或指令，例如 "请编写一个排序算法"。
        timeout (float, optional): 放入队列的超时时间（秒）。默认为 None 表示无限等待。
                                   如果队列满且设置了 timeout，超时后会抛出异常。

    Returns:
        str: 成功时返回包含 task_id 的确认字符串，例如 "任务已发布，ID: xxxxxxxx"；
             失败时返回描述错误的字符串。
    """
    try:
        # 生成唯一任务 ID
        task_id = str(uuid.uuid4())

        # 将 task_id 和 task_msg 放入队列（框架会打包）
        if timeout is not None:
            queue_coder.put((task_id, task_msg), block=True, timeout=timeout)
        else:
            queue_coder.put((task_id, task_msg))

        return f"任务已发布，ID: {task_id}"
    except Exception as e:
        return f"错误：发布任务失败: {e}"