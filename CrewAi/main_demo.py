import sys
from crew import SoporteIncidenciasCrew 

def run():
    """
    SCRIPT PARA PRUEBAS: Lee una incidencia desde un fichero y pone en marcha el crew para analizarla.
    """
    try:
        with open('incidencia.txt', 'r', encoding='utf-8') as file:
            incidencia_texto = file.read()
    except FileNotFoundError:
        print("Error: No se encontró el fichero con la incidencia de prueba.")
        print("Por favor, crea el fichero y asegurate que se llame 'incidencia.txt'")
        sys.exit(1)

    inputs = {
        'incidencia': incidencia_texto,
        'cat': "Redes, Hardware, Software, Cuentas de usuario, Permisos",
        'url_a_verificar': 'google.com' 
    }

    SoporteIncidenciasCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()