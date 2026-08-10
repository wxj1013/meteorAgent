from config import Config
from coder import Coder
from .tool import assign_to
import subprocess
import sys
from pathlib import Path
from utils import parse_size
import traceback

@assign_to(Coder)
def run_python(script_path: str, args: list = None) -> str:
    """
    运行 workspace 下指定的 Python 脚本，并捕获其控制台输出（stdout + stderr）。

    此工具专为大模型执行 Python 脚本后分析输出结果而设计。
    执行前会检查文件是否存在、是否可执行，并限制执行时间和输出大小，
    避免长时间阻塞或占用过多 token。

    Args:
        script_path (str): 相对于 工作空间 的 Python 脚本路径，例如 "scripts/train.py"。
        args (list, optional): 传递给脚本的命令行参数列表，例如 ["--epochs", "10"]。

    Returns:
        str: 脚本的标准输出与标准错误合并后的文本（成功），或描述错误的字符串（失败）。
              可根据返回内容判断下一步操作。
    """
    try:
        workspace = Config.get("env").get("workspace")
        target_path = Path(workspace) / script_path

        # 检查文件是否存在
        if not target_path.exists():
            return f"错误：文件 {target_path} 不存在"

        # 检查是否为 Python 文件（简单后缀校验）
        if target_path.suffix != ".py":
            return f"错误：文件 {target_path} 不是 .py 文件，无法执行"

        # 最大输出字节数（可选，默认 1MB）
        max_output = parse_size(
            Config.get("tool").get("system_command").get("run_python").get("output_limit")
        )

        # 超时时间（秒）
        timeout = Config.get("tool").get("system_command").get("run_python").get("timeout")

        # 准备命令行
        cmd = [sys.executable, str(target_path)]
        if args:
            cmd.extend(args)

        # 执行脚本，捕获输出
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=timeout,
            cwd=str(target_path.parent)  # 在脚本所在目录执行
        )

        # 合并 stdout 和 stderr
        output = (result.stdout or '') + (result.stderr or '')

        # 截断过长的输出
        if len(output.encode("utf-8")) > max_output:
            truncated = True
            # 按字符截断到 max_output 字节以内（近似）
            while len(output.encode("utf-8")) > max_output:
                output = output[:-100]
            output += "\n... (输出已被截断，因为超过最大大小限制)"
        else:
            truncated = False

        # 附加返回码信息（非零时提示）
        if result.returncode != 0:
            output += f"\n进程退出码：{result.returncode}"

        return output

    except subprocess.TimeoutExpired:
        return f"错误：脚本执行超时（{timeout} 秒），请检查代码或增加 timeout 参数"
    except FileNotFoundError:
        return f"错误：找不到 Python 解释器（{sys.executable}），请确认环境配置"
    except Exception as e:
        error_detail = traceback.format_exc()
        return f"执行脚本失败：{str(error_detail)}"