from role import Role
from config import Config
from pathlib import Path
import threading
from agents import register

current_dir = Path(__file__).parent
prompt_path = current_dir / 'prompt.md'
prompt = prompt_path.read_text(encoding='utf-8')

"""
    编码者，负责核心代码编写
"""
class Coder(Role):
    _name: str = "coder"
    _system_prompt = prompt

# 读取配置，初始化角色
cfg = Config.get("coder")

def _run(name, conf):
    coder = Coder(
        conf['api_key'],
        conf['llm_model'],
        conf['reasoning_effort'],
        conf['max_iteration'],
        conf['max_retry'],
        name
    )
    coder.run(10)

# 多线程启动
for name, conf in cfg.items():
    t = threading.Thread(
        target=_run,
        args=(name, conf),
        name=f"Coder-{name}",
        daemon=True          
    )
    t.start()
    register(name, t)

