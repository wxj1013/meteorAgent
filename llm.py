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
    def __init__(self, api_key: str, model: str, reasoning_effort: str, system_prompt: str):
        self.api_key = api_key
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.system_prompt = system_prompt
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com")

    # agent角色与用户
    def chat(self, message: str) -> str:
        # 组装message
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message},
        ]

        # 发送请求
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False, 
            reasoning_effort=self.reasoning_effort,
            extra_body={"thinking": {"type": "enabled"}}
        )
        return response.choices[0].message.content

