from pathlib import Path
from config import Config

worksp
path = Path(workspace)

@assign_to(Coder)
def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    读取 workspace 下指定文本文件的全部内容（带大小限制）。

    此工具专为大模型全量读取文件后直接修改代码而设计。
    读取前会检查文件大小是否超过预设阈值 `read_file_size`，
    若超出则拒绝读取并返回错误信息，避免占用过多 token 或导致超时。

    Args:
        file_path (str): 相对于 工作空间 的文件路径，例如 "src/main.py"。
        encoding (str, optional): 文件编码，默认 "utf-8"。

    Returns:
        str: 文件完整内容（成功），或描述错误的字符串（失败）。
              大模型可根据返回内容判断下一步操作。
    """
    try:
        workspace = Config.get("env").get("workspace")

        max_size = Config.get("read_file_size", 5 * 1024 * 1024)  # 默认 5MB
        target_path = Path(workspace) / file_path

        # 检查文件是否存在
        if not target_path.exists():
            return f"错误：文件 {target_path} 不存在"

        # 检查文件大小
        file_size = target_path.stat().st_size
        if file_size > max_size:
            return (
                f"错误：文件过大 ({file_size} bytes)，超过允许的最大值 {max_size} bytes。"
                f"建议增大 read_file_size 配置或使用其他工具处理文件。"
            )

    # 尝试读取文件
        with open(target_path, "r", encoding=encoding) as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        return f"错误：文件 {target_path} 编码不是 {encoding}，请检查或更换 encoding 参数"
    except Exception as e:
        return f"读取文件失败：{str(e)}"

@assign_to(Coder)
def write_file(file_path: str, content: str, encoding: str = "utf-8") -> str:
    """
    	写入文本文件（覆盖写入）
    """
    try:
        # 自动创建目录
        dir_path = path.dirname(file_path)
        if dir_path and not path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return f"成功写入文件：{file_path}"
    except Exception as e:
        return f"写入文件失败：{str(e)}"

@assign_to(Coder)
def list_all_files() -> str:
    """
    列举指定目录下的所有文件。

    Args:
        directory (str): 目标目录路径。
        recursive (bool): 是否递归遍历子目录。默认为 True。

    Returns:
        str: 包含文件完整路径的列表,用逗号连接。
    """
    files = []
    for entry in path.rglob('*'):
        if entry.is_file():
            files.append(str(entry.resolve()))

    return "".join(files)