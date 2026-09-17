'''
import torch 

cuda_version = torch.version.cuda
print(f"CUDA Version: {cuda_version}")

# 获取当前GPU的名称
gpu_name = torch.cuda.get_device_name()
print(f"GPU Name: {gpu_name}")
'''


# from role import Role
# from coder import Coder
# from config import Config
# import tools
# from llm import DeepSeekLLM
# from log import Logger

# print(Coder.handle_task("任务来自planner。\n完成如下代码：使用CNN完成对/data/cifar-10-batches-py中数据集的分类。"))


from utils import MessageCenter

MC = MessageCenter("localhost", 7777)

id1 = MC.publish_task("coder", "这是一条任务")

# print(id1)
# 1dc601e1-c75c-4949-9ac4-3d8a8789d1ce

t = MC.fetch_task("coder")
print(t.task_id)
print(t.content)

MC.report_result(id1, "任务完成987")

res = MC.fetch_result(id1)

print(res)