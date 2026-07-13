import json
from .models import Action
from config import env

class MLPlanner:
    async def plan(self, goal: str, history: list) -> Action:
        """
        目前用 Mock 返回固定 JSON，验证链路。
        后续替换为真实 LLM 调用，只需改这个方法体。
        """
        # ===== Mock 响应（模拟 DeepSeek 返回）=====
        mock_response = {
            "thought": f"Goal is '{goal}'. packs are available ({env.get('packages')}), "
                       f"GPU is {env.get('cuda')}. I will write a training script.",
            "tool": "write_file",
            "args": {
                "path": "./train.py",
                "content": "import torch\nprint('training...')"
            }
        }
        # ==========================================

        # 解析并校验
        action = Action(**mock_response)
        return action