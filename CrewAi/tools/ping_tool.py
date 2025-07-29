import subprocess
from crewai.tools import tool

@tool("Ping Tool")
def ping_tool(url: str) -> str:
    """
    Mide la latencia de una URL para comprobar su disponibilidad y
    tiempo de respuesta.
    """
    try:
        # El comando '-c 4' envía 4 paquetes, es una práctica estándar.
        result = subprocess.run(
            ['ping', '-c', '4', url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar el ping: {e.stderr}"
    except FileNotFoundError:
        return "Error: No se encontró el comando 'ping'. Asegúrate de que esté instalado y en tu PATH."