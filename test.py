'''
import torch 

cuda_version = torch.version.cuda
print(f"CUDA Version: {cuda_version}")

# 获取当前GPU的名称
gpu_name = torch.cuda.get_device_name()
print(f"GPU Name: {gpu_name}")
'''


from role import Role
from coder import Coder
from config import Config
import tools
from llm import DeepSeekLLM

dsllm = DeepSeekLLM("sk-8f026b1a113b4c428f0b1e58eb1e7eee", "deepseek-v4-pro", "high", "你是一个测试llm功能返回的机器人，可以随便回复")

# print(dsllm.chat("复活吧我的爱人"))