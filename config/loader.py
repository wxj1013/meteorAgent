import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    """
    统一配置加载器（单例模式）
    所有模块都从这里读配置
    """
    _instance = None
    _data: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_all()
        return cls._instance

    def _load_all(self):
        base = Path(__file__).parent
        for yml in base.glob("*.yaml"):
            with open(yml, "r", encoding="utf-8") as f:
                self._data[yml.stem] = yaml.safe_load(f)

    # ---------- 通用接口 ----------
    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def env(self):
        return self._data.get("env", {})

    def orchestrator(self):
        return self._data.get("orchestrator", {})

    def agent(self):
        return self._data.get("agent", {})

    # ---------- 快捷访问 ----------
    def __getitem__(self, item):
        return self._data[item]