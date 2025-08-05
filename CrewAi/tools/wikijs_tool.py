import requests
from crewai.tools import tool

#Configuración
WIKIJS_URL = "URL"
WIKIJS_API_TOKEN = "INSERT_API"

@tool("Wiki.js Tool")
def wikijs_tool(search_query: str) -> str:
    """
    Busca en la base de conocimiento de Wiki.js para encontrar páginas
    relevantes a la consulta de búsqueda.
    """
    if WIKIJS_URL == "URL_DE_TU_WIKIJS":
        return "Error: La URL de Wiki.js no ha sido configurada. Por favor, edita el fichero tools/wikijs_tool.py."

    graphql_endpoint = f"{WIKIJS_URL}/graphql"

    graphql_query = """
        query($query: String!) {
            pages {
                search(query: $query, path: "") {
                    results {
                        id
                        path
                        title
                        description
                    }
                }
            }
        }
    """

    headers = {
        "Authorization": f"Bearer {WIKIJS_API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "query": graphql_query,
        "variables": {
            "query": search_query
        }
    }

    try:
        response = requests.post(graphql_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            return f"Error en la respuesta de la API de Wiki.js: {data['errors']}"

        search_results = data.get("data", {}).get("pages", {}).get("search", {}).get("results", [])

        if not search_results:
            return f"No se encontraron resultados en Wiki.js para: '{search_query}'"

        # Formatear los resultados
        output = f"Resultados de la búsqueda en Wiki.js para '{search_query}':\n\n"
        for i, result in enumerate(search_results):
            title = result.get("title")
            path = result.get("path")
            description = result.get("description")
            output += f"{i+1}. **{title}**\n   - Descripción: {description}\n   - Ruta: /{path}\n\n"

        return output

    except requests.exceptions.RequestException as e:
        return f"Error al conectar con la API de Wiki.js: {e}"
    except Exception as e:
        return f"Ha ocurrido un error inesperado: {e}"