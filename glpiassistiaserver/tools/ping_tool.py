import subprocess
import platform
from urllib.parse import urlparse
from crewai.tools import tool

@tool("Ping Tool")
def ping_tool(url: str) -> str:
    """
    Mide la latencia de una URL para comprobar su disponibilidad y tiempo de respuesta.
    Extrae el hostname de la URL antes de hacer ping.
    """
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if not hostname:
            hostname = url.split('//')[-1].split('/')[0]

        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', hostname]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or e.stdout
        return f"Error al ejecutar el ping a '{hostname}': {error_output}"
    except FileNotFoundError:
        return "Error: No se encontró el comando 'ping'. Asegúrate de que esté instalado y en tu PATH."
    except Exception as e:
        return f"Ha ocurrido un error inesperado en la herramienta de ping: {str(e)}"