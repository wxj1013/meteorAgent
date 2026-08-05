from typing import Callable
import inspect

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


# 注册工具权限，注册后的role可以通过call_tool来使用。
def assign_to(*role_classes: type):
    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)
        # 返回类型必须为str
        return_annotation = sig.return_annotation
        if return_annotation is not str:
            raise TypeError(f"函数 {func.__name__} 的返回类型注解必须是 str")
        # 注册工具
        tool = Tool(
            func=func,
            parameters=list(sig.parameters.values()), 
            returns=sig.return_annotation,
            doc=func.__doc__
        )
        for role_cls in role_classes:
            role_cls._tools.append(tool)
        return func
    return decorator