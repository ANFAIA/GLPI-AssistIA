# server.py

import asyncio
import json
import sys
import logging
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod

from registry import tool_registry  # Usamos la instancia compartida

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MCPRequest:
    jsonrpc: str
    id: Optional[str]
    method: str
    params: Optional[Dict[str, Any]] = None


@dataclass
class MCPResponse:
    jsonrpc: str
    id: Optional[str]
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class MCPError:
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPServer:
    """Custom MCP Server implementation"""

    def __init__(self, name: str):
        self.name = name
        self.registry = tool_registry  # Importado desde registry.py
        self.capabilities = {
            "tools": {},
            "logging": {},
            "prompts": {},
            "resources": {}
        }

    def tool(self, name: str, description: str, parameters: Dict[str, Any] = None):
        """Decorator to register tools"""
        def decorator(func: Callable):
            schema = {
                "name": name,
                "description": description,
                "inputSchema": {
                    "type": "object",
                    "properties": parameters or {},
                    "required": list(parameters.keys()) if parameters else []
                }
            }
            self.registry.register_tool(name, func, schema)
            return func
        return decorator

    async def handle_request(self, request_data: str) -> str:
        try:
            request_json = json.loads(request_data)
            request = MCPRequest(
                jsonrpc=request_json.get("jsonrpc", "2.0"),
                id=request_json.get("id"),
                method=request_json["method"],
                params=request_json.get("params")
            )
            response = await self._route_request(request)
            return json.dumps(asdict(response), separators=(',', ':'))
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return json.dumps(asdict(MCPResponse(
                jsonrpc="2.0",
                id=request_json.get("id") if 'request_json' in locals() else None,
                error=asdict(MCPError(
                    code=-32603,
                    message="Internal error",
                    data={"error": str(e)}
                ))
            )), separators=(',', ':'))

    async def _route_request(self, request: MCPRequest) -> MCPResponse:
        method = request.method

        if method == "initialize":
            return await self._handle_initialize(request)
        elif method == "tools/list":
            return await self._handle_tools_list(request)
        elif method == "tools/call":
            return await self._handle_tools_call(request)
        elif method == "ping":
            return await self._handle_ping(request)
        else:
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                error=asdict(MCPError(
                    code=-32601,
                    message=f"Method not found: {method}"
                ))
            )

    async def _handle_initialize(self, request: MCPRequest) -> MCPResponse:
        return MCPResponse(
            jsonrpc="2.0",
            id=request.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": self.capabilities,
                "serverInfo": {
                    "name": self.name,
                    "version": "1.0.0"
                }
            }
        )

    async def _handle_tools_list(self, request: MCPRequest) -> MCPResponse:
        return MCPResponse(
            jsonrpc="2.0",
            id=request.id,
            result={
                "tools": self.registry.get_all_tools()
            }
        )

    async def _handle_tools_call(self, request: MCPRequest) -> MCPResponse:
        if not request.params:
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                error=asdict(MCPError(
                    code=-32602,
                    message="Invalid params"
                ))
            )

        tool_name = request.params.get("name")
        tool_args = request.params.get("arguments", {})

        tool_func = self.registry.get_tool(tool_name)
        if not tool_func:
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                error=asdict(MCPError(
                    code=-32601,
                    message=f"Tool not found: {tool_name}"
                ))
            )

        try:
            result = await tool_func(**tool_args) if asyncio.iscoroutinefunction(tool_func) else tool_func(**tool_args)

            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                result={
                    "content": [{
                        "type": "text",
                        "text": str(result)
                    }]
                }
            )
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                error=asdict(MCPError(
                    code=-32603,
                    message=f"Tool execution error: {str(e)}"
                ))
            )

    async def _handle_ping(self, request: MCPRequest) -> MCPResponse:
        return MCPResponse(jsonrpc="2.0", id=request.id, result={})

    async def run_stdio(self):
        logger.info(f"Starting MCP server: {self.name}")
        logger.info("Listening on stdio...")

        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break

                line = line.strip()
                if not line:
                    continue

                response = await self.handle_request(line)
                print(response, flush=True)

            except KeyboardInterrupt:
                logger.info("Server shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")


# Crear instancia del servidor
mcp_server = MCPServer("mix_server")

# Cargar herramientas (al importar, se registran automáticamente en tool_registry)
try:
    from tools import hello
    logger.info("Tools imported successfully")
except ImportError as e:
    logger.error(f"Error importing tools: {e}")


# Punto de entrada
if __name__ == "__main__":
    asyncio.run(mcp_server.run_stdio())
