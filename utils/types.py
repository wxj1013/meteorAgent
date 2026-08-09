import inspect

# python类转为json类
def py_type_to_json(py_type) -> str:
    """Python 类型转 JSON Schema 类型"""
    if py_type == inspect.Parameter.empty:
        return "string"
    return {
        str: "string", int: "integer", float: "number",
        bool: "boolean", list: "array", dict: "object"
    }.get(py_type, "string")