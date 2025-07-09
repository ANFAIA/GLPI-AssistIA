# tool_registry.py
from typing import Dict, Any, Callable, List
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Registry for MCP tools"""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, func: Callable, schema: Dict[str, Any]):
        self.tools[name] = func
        self.tool_schemas[name] = schema
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Callable:
        return self.tools.get(name)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        return list(self.tool_schemas.values())