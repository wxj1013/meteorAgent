from pathlib import Path
from config import Config
from utils import parse_size
from coder import Coder
from .tool import assign_to

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
              可根据返回内容判断下一步操作。
    """
    try:
        workspace = Config.get("env").get("workspace") # 工作空间

        max_size = parse_size(Config.get("tool").get("file_operation").get("read_file").get("size_limit")) # 读取文件限制
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
    将文本内容覆盖写入 workspace 下的指定文件（自动创建父目录）。

    写入前会检查文件所在目录是否存在，若不存在则自动创建。
    写入完成后返回成功信息；若写入过程中出现异常，返回错误描述。

    Args:
        file_path (str): 相对于 工作空间 的文件路径，例如 "output/result.txt"。
        content (str):  要写入的文本内容。
        encoding (str, optional): 文件编码，默认 "utf-8"。

    Returns:
        str: 成功时返回 "成功写入文件：<绝对路径>"，失败时返回错误描述字符串。
    """
    try:
        workspace = Config.get("env").get("workspace")
        target_path = Path(workspace) / file_path

        # 自动创建父目录
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, "w", encoding=encoding) as f:
            f.write(content)

        return f"成功写入文件：{target_path}"
    except Exception as e:
        return f"写入文件失败：{str(e)}"


@assign_to(Coder)
def list_all_files() -> str:
    """
    列举 workspace 下指定目录内的所有文件（包括文件夹中的文件）。


    Args:

    Returns:
        str: 文件路径列表，用逗号连接（路径为相对于工作空间的相对路径）。
             若目录不存在或发生其他错误，返回对应的错误描述字符串。
    """
    try:
        path = Path(Config.get("env").get("workspace"))

        files = []
        iterator = path.rglob("*")

        for entry in iterator:
            if entry.is_file():
                # 返回相对于 workspace 的相对路径，方便后续配合 read_file 使用
                rel_path = entry.relative_to(path)
                files.append(str(rel_path))

        return ",".join(files)
    except Exception as e:
        return f"列举文件失败：{str(e)}"