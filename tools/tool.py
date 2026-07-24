from typing import Callable

"""
    agent工具
"""
class Tool:
    def __init__(self, func: Callable, 
                 parameters: str, returns: str, doc: str):
        self.func = func
        self.name = func.__name__
        self.parameters = parameters   # 入参
        self.returns = returns         # 出参
        self.doc = doc                 # 注释

    def to_natural_language(self) -> str:
        """返回该工具的自然语言描述"""
        return (
            f"工具名称：{self.name}\n"
            f"输入参数：{self.parameters}\n"
            f"输出结果：{self.returns}\n"
            f"注释：{self.doc}\n"
        )