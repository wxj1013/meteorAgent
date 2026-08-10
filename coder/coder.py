from role import Role
from config import Config
from pathlib import Path

"""
	编码者，负责核心代码编写
"""
class Coder(Role):
	_name: str = "coder"
	_max_iteration = Config.get("coder").get("max_iteration")

# 初始化llm模型
llm_model = Config.get("coder").get("llm_model")
api_key = Config.get("coder").get("api_key")
reasoning_effort = Config.get("coder").get("reasoning_effort")

# 获得coder的prompt
current_dir = Path(__file__).parent
file_path = current_dir / 'prompt.md'
prompt = file_path.read_text(encoding='utf-8')
Coder.init_llm_model(api_key, llm_model, reasoning_effort, prompt)
