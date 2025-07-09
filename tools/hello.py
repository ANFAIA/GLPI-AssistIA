from registry import tool_registry

def register_tool(name: str, description: str, parameters: dict = None):
    def decorator(func):
        schema = {
            "name": name,
            "description": description,
            "inputSchema": {
                "type": "object",
                "properties": parameters or {},
                "required": list(parameters.keys()) if parameters else []
            }
        }
        tool_registry.register_tool(name, func, schema)
        return func
    return decorator


@register_tool(name="say_hello", description="Say hello", parameters={"name": {"type": "string"}})
def say_hello(name: str):
    return f"Hello, {name}!"