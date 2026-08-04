import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    """
        全局配置类，启动时加载。
        读取所有.yaml类
        使用方法(例如env.yaml)：
        from config import Config
        env = Config.get("env")
    """
    _data: Dict[str, Any] = {}

    @classmethod
    def load(cls):
        base = Path(__file__).parent
        for yml in base.glob("*.yaml"):
            with open(yml, "r", encoding="utf-8") as f:
                cls._data[yml.stem] = yaml.safe_load(f)

    @classmethod
    def get(cls, key: str):
        return cls._data.get(key)

    @classmethod
    def set(cls, key: str, value):
        cls._data[key] = value


# 导入即加载
Config.load()