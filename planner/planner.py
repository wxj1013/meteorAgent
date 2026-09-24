from role import Role
from pathlib import Path
from config import Config
import multiprocessing

current_dir = Path(__file__).parent
prompt_path = current_dir / 'prompt.md'
prompt = prompt_path.read_text(encoding='utf-8')

# 配置读取
llm_model = Config.get("planner").get("llm_model")
api_key = Config.get("planner").get("api_key")
reasoning_effort = Config.get("planner").get("reasoning_effort")
max_iteration = Config.get("planner").get("max_iteration")
max_retry = Config.get("planner").get("max_retry")
timeout = Config.get("planner").get("timeout") # TODO,暂未实现timeout


"""
    总负责人
"""
class Planner(Role):
	_name: str = "planner"
	_system_prompt = prompt

planner = Planner(api_key, llm_model, reasoning_effort, max_iteration, max_retry, "planner")

def run_planner():
    planner.run(poll_interval=10)

multiprocessing.Process(target=run_planner, daemon=True).start()