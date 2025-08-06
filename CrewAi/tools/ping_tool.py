import subprocess
import platform 
from crewai.tools import tool

@tool("Ping Tool")
def ping_tool(url: str) -> str:
    """
    Mide la latencia de una URL para comprobar su disponibilidad y tiempo de respuesta.
    """
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', url]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar el ping: {e.stderr}"
    except FileNotFoundError:
        return "Error: No se encontró el comando 'ping'. Asegúrate de que esté instalado y en tu PATH."