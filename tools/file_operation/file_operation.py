from pathlib import Path

path = Path(workdir)

@assign_to(Coder)
def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    	读取文本文件内容
    """
    if not path.exists(file_path):
        return f"错误：文件 {file_path} 不存在"
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return content
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