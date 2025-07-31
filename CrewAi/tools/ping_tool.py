import subprocess
import platform  # 1. Importa la librería 'platform'
from crewai.tools import tool

@tool("Ping Tool")
def ping_tool(url: str) -> str:
    """
    Mide la latencia de una URL para comprobar su disponibilidad y
    tiempo de respuesta.
    """
    try:
        # 2. Elige el parámetro correcto según el sistema operativo
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        
        # 3. Construye y ejecuta el comando
        command = ['ping', param, '4', url]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Ahora el mensaje de error será más completo
        return f"Error al ejecutar el ping: {e.stderr}"
    except FileNotFoundError:
        return "Error: No se encontró el comando 'ping'. Asegúrate de que esté instalado y en tu PATH."