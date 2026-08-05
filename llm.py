# 大模型类
from typing import List, Dict
from openai import OpenAI

# LLM基类
class BaseLLM:
    """大模型基类，所有 LLM 需实现 chat 方法"""
    def chat(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError

# deepseek
class DeepSeekLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, stream: bool):
        self.api_key = api_key
        self.model = model
        self.stream = stream
        self.reasoning_effort = reasoning_effort
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=self.stream,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )
        return response

