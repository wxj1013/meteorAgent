import pickle
import uuid
from typing import Optional

import yaml
import redis

from task import Task


class MessageCenter:
    """消息中心客户端，基于 Redis List + pickle 序列化"""

    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)["message_center"]

        redis_cfg = {
            "host": cfg["host"],
            "port": cfg["port"],
            "db": 0,
            "socket_timeout": 0,
            "decode_responses": False,          # 必须 False，传输 bytes
        }
        if cfg.get("password"):
            redis_cfg["password"] = cfg["password"]

        self._client = redis.Redis(**redis_cfg)

        self.task_result = {}

    # 发布向指定queue发布一个任务
    def publish_task(self, queue: str, content: str) -> str:
        task_id = str(uuid.uuid4())
        task = Task(task_id=task_id, content=content)
        data = pickle.dumps(task)
        if queue not in ["planner", "coder", "analyst", "engineer", "tester"]:
            return f"错误：队列:{queue}不存在"
        self._client.rpush(queue, data)
        return task_id

    # 获取一个任务
    def fetch_task(self, queue: str) -> Optional[Task]:
        result = self._client.blpop(queue, timeout=0)
        if result is None:
            return None
        _, data = result
        return pickle.loads(data)

    # 完成任务并回报给planner
    def report_result(self, task_id: str, result: object):
        task = Task(task_id=task_id, result=result)
        data = pickle.dumps(task)
        self._client.rpush(self.result_queue, data)

    #  清空队列
    def clear_queues(self):
        self._client.delete("planner", "coder", "analyst", "engineer", "tester")