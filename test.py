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

# print(Coder._llm_model.system_prompt)

print(Coder.pack_tools())
