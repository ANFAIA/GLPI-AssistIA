#---------------------------------------------------
# Intento de implementación de Groq (API) - EN OBRAS
#---------------------------------------------------
import sys
from crew_groq import SoporteIncidenciasCrewGroq 

def run():
    """
    SCRIPT PARA PRUEBAS CON GROQ: Lee una incidencia desde un fichero y pone 
    en marcha el crew para analizarla usando la API de Groq.
    """
    try:
        with open('incidencia.txt', 'r', encoding='utf-8') as file:
            incidencia_texto = file.read()
    except FileNotFoundError:
        print("Error: No se encontró el fichero 'incidencia.txt'.")
        sys.exit(1)

    inputs = {
        'incidencia': incidencia_texto,
        'cat': "Redes, Hardware, Software, Cuentas de usuario, Permisos",
        'url_a_verificar': 'google.com' 
    }

    SoporteIncidenciasCrewGroq().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()