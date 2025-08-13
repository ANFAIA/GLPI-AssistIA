import requests

WIKIJS_URL = os.getenv("WIKIJS_URL")
WIKIJS_API_TOKEN = os.getenv("WIKIJS_API_TOKEN")

def search_wiki(search_query: str) -> str:
    """
    Realiza una búsqueda en la base de conocimiento de Wiki.js a través de su API GraphQL.
    """
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
        response = requests.post(graphql_endpoint, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            return f"Error en la respuesta de la API de Wiki.js: {data['errors']}"

        search_results = data.get("data", {}).get("pages", {}).get("search", {}).get("results", [])

        if not search_results:
            return f"No se encontraron resultados en la base de conocimiento para: '{search_query}'"

        output = f"Resultados de la búsqueda en la base de conocimiento para '{search_query}':\n\n"
        for i, result in enumerate(search_results):
            title = result.get("title")
            path = result.get("path")
            description = result.get("description")
            output += f"{i+1}. **{title}**\n   - Descripción: {description}\n   - Ruta: /{path}\n\n"

        return output

    except requests.exceptions.RequestException as e:
        return f"Error de comunicación con el servidor de Wiki.js: {e}"
    except Exception as e:
        return f"Ha ocurrido un error inesperado en el manejador de Wiki.js: {e}"