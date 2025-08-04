import requests
from crewai.tools import tool

MCP_SERVER_URL = "http://localhost:8000/buscar_en_wiki"

@tool("Wiki.js Knowledge Base Tool")
def wikijs_mcp_tool(search_query: str) -> str:
    """
    Utiliza esta herramienta para buscar en la base de conocimiento interna de Wiki.js.
    """
    try:
        response = requests.get(MCP_SERVER_URL, params={"query": search_query})
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        return f"Error de comunicación con el servidor: {e}"
    except Exception as e:
        return f"Error inesperado en la herramienta Wiki.js: {e}"