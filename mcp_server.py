from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from glpiassistiaserver.tools.mcp_tools.wiki_handler import search_wiki
from fastapi import Query

from glpiassistiaserver.tools.glpi_tool import router as glpi_router

app = FastAPI()

@app.get("/buscar_en_wiki")
def buscar_en_wiki(query: str = Query(..., min_length=1)) -> str:
    """Herramienta que busca en la base de conocimiento de Wiki.js."""
    print(f"MCP Server: Recibida petición para buscar en la wiki: '{query}'")
    return search_wiki(query)

# MONTA GLPI
app.include_router(glpi_router)

@app.get("/")
def read_root():
    return {"message": "Servidor principal funcionando"}

mcp = FastApiMCP(app)
mcp.mount_http()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
