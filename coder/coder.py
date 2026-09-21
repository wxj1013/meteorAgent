from role import Role
from config import Config
from pathlib import Path
import threading
import time

"""
	编码者，负责核心代码编写
"""
class Coder(Role):
	_name: str = "coder"

"""
# 初始化llm模型
llm_model = Config.get("coder").get("llm_model")
api_key = Config.get("coder").get("api_key")
reasoning_effort = Config.get("coder").get("reasoning_effort")

# 获得coder的prompt
current_dir = Path(__file__).parent
file_path = current_dir / 'prompt.md'
prompt = file_path.read_text(encoding='utf-8')
Coder.init_llm_model(api_key, llm_model, reasoning_effort, prompt)
"""

"""
# 运行编码者
def run_coder(role: Role):
    try:
        role.run(poll_interval=1.0)
    except Exception as e:
        Logger.error(f"角色 {role._name} 异常退出: {e}")

# 创建线程
threads = [
    threading.Thread(target=run_with_exception_guard, args=(researcher,), daemon=True),
    threading.Thread(target=run_with_exception_guard, args=(coder,), daemon=True),
]

# 启动
for t in threads:
    t.start()

# 主线程等待（如果希望程序常驻）
for t in threads:
    t.join()
"""


"""
from concurrent.futures import ThreadPoolExecutor

roles = [
    Researcher(api_key="..."),
    Coder(api_key="..."),
    Role(api_key="...", name="reviewer"),
]

with ThreadPoolExecutor(max_workers=len(roles)) as executor:
    futures = [executor.submit(run_with_exception_guard, role) for role in roles]
    # 等待所有角色结束（会一直运行，除非手动停止）
    for f in futures:
        f.result()
"""