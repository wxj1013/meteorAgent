from role import Role
from pathlib import Path
from config import Config

current_dir = Path(__file__).parent
prompt_path = current_dir / 'prompt.md'
prompt = prompt_path.read_text(encoding='utf-8')

"""
    总负责人
"""
class Planner(Role):
	_name: str = "planner"
	_system_prompt = prompt

planner = Planner(poll_interval = 10.0)