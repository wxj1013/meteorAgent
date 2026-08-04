"""
	文件相关的util函数
"""

# 解析B,KB,MB,GB形式的文件大小
def parse_size(size_str: str) -> int:
    """将 '5KB', '5MB', '5GB' 等转换为字节数"""
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    size_str = size_str.strip().upper()
    for unit in ["GB", "MB", "KB", "B"]:
        if size_str.endswith(unit):
            num = float(size_str[:-len(unit)])
            return int(num * units[unit])
    raise ValueError(f"无法解析文件大小: {size_str}")