import socket
import pickle
import uuid
from typing import Optional
import io
from config import Config

# Task类
class Task:
    def __init__(self, task_id=None, content=None):
        self.task_id = task_id
        self.content = content
        self.historys = []
        self.sub_tasks = []

class MyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # 服务端序列化时类在 task.Task，这里映射到本模块的 Task
        if module == "task" and name == "Task":
            return Task
        return super().find_class(module, name)

class MessageCenter:
    def __init__(self, host="localhost", port=7777):
        self.host = host
        self.port = port

    def _send(self, cmd, args=None):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(pickle.dumps((cmd, args)))
            resp = sock.recv(8192)
            return pickle.loads(resp)

    def publish_task(self, queue: str, content: str) -> str:
        resp = self._send("publish", (queue, content))
        if resp.get("ok"):
            return resp["task_id"]
        raise Exception(resp.get("error", "unknown error"))

    def fetch_task(self, queue: str) -> Optional[Task]:
        resp = self._send("fetch", queue)
        if resp.get("ok") and resp.get("data") is not None:
            return MyUnpickler(io.BytesIO(resp["data"])).load()
        return None

    def report_result(self, task_id: str, result: str):
        self._send("report", (task_id, result))

    def fetch_result(self, task_id: str):
        resp = self._send("result", task_id)
        if resp.get("ok"):
            return resp["data"]
        return None

host = Config.get("env").get("queues").get("host")
port = Config.get("env").get("queues").get("port")

mc = MessageCenter(host, port)
        