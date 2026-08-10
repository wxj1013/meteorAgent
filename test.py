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
from log import Logger

print(Coder.handle_task("任务来自planner。\n完成如下代码：使用CNN完成对/data/cifar-10-batches-py中数据集的分类。"))

