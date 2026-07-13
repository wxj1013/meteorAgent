import torch 

cuda_version = torch.version.cuda
print(f"CUDA Version: {cuda_version}")

# 获取当前GPU的名称
gpu_name = torch.cuda.get_device_name()
print(f"GPU Name: {gpu_name}")