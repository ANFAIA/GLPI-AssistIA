#Este script pone en marcha un servidor MCP utilizando FastAPI. (En pruebas)
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP  
from mcp_tools.wiki_handler import search_wiki

app = FastAPI()
@app.get("/buscar_en_wiki")
def buscar_en_wiki(query: str) -> str:
    """
    Herramienta que busca en la base de conocimiento de Wiki.js.
    """
    print(f"MCP Server: Recibida petición para buscar en la wiki: '{query}'")
    return search_wiki(query)

@app.get("/")
def read_root():
    return {"message": "Servidor principal funcionando"}

mcp = FastApiMCP(app)
mcp.mount_http()