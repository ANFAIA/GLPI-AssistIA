import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de GLPI - Actualmente estamos usando un ticket de prueba, por lo que no estableceremos conexión con GLPI
GLPI_URL = os.getenv('GLPI_URL', 'https://mi-servidorglpi.com (PRUEBA)')
GLPI_APP_TOKEN = os.getenv('GLPI_APP_TOKEN', 'un_token_de_acceso')
GLPI_USER_TOKEN = os.getenv('GLPI_USER_TOKEN', 'un_usuario_cualquiera')

# Configuración de Ollama
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'phi3:mini') #Usamos este modelo debido a su tamaño reducido