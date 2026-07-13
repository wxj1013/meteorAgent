import yaml
from pathlib import Path

_CONFIG_DIR = Path(__file__).parent

def _load_yaml(name: str) -> dict:
    path = _CONFIG_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 全局可访问的配置
env = _load_yaml("env.yaml")