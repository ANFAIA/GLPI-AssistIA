#---------------------------------------------------
# Implementación de Cerebras (API)
#---------------------------------------------------
import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_cerebras import ChatCerebras

script_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(script_dir, '.env.cerebras')
load_dotenv(dotenv_path=dotenv_path)

from tools.ping_tool import ping_tool
from tools.wikijs_mcp_tool import wikijs_mcp_tool

@CrewBase
class SoporteIncidenciasCrewCerebras():
    """
    Crew para gestionar y resolver incidencias de soporte técnico usando la API de Cerebras.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        """
        Inicializa el Crew con el modelo de Cerebras.
        """
        self.llm = ChatCerebras(
            api_key=os.environ.get("CEREBRAS_API_KEY"),
            # --- CORRECCIÓN AQUÍ ---
            model="cerebras/llama-3.3-70b"
        )

    @agent
    def analista_sentimiento(self) -> Agent:
        """
        Agente que analiza el sentimiento de la incidencia.
        """
        return Agent(config=self.agents_config['analista_sentimiento'], llm=self.llm, verbose=True)

    @agent
    def clasificador_incidencias(self) -> Agent:
        """
        Agente que clasifica la incidencia en una categoría técnica.
        """
        return Agent(config=self.agents_config['clasificador_incidencias'], llm=self.llm, verbose=True)

    @agent
    def buscador_soluciones(self) -> Agent:
        """
        Agente que busca soluciones en la base de conocimiento.
        """
        return Agent(
            config=self.agents_config['buscador_soluciones'],
            llm=self.llm,
            tools=[ping_tool, wikijs_mcp_tool],
            verbose=True
        )

    @task
    def analizar_sentimiento_task(self) -> Task:
        """
        Tarea de análisis de sentimiento.
        """
        return Task(config=self.tasks_config['analizar_sentimiento_task'], agent=self.analista_sentimiento())

    @task
    def clasificar_incidencia_task(self) -> Task:
        """
        Tarea de clasificación de la incidencia.
        """
        return Task(config=self.tasks_config['clasificar_incidencia_task'], agent=self.clasificador_incidencias())

    @task
    def buscar_soluciones_task(self) -> Task:
        """
        Tarea de búsqueda de soluciones.
        """
        return Task(
            config=self.tasks_config['buscar_soluciones_task'],
            agent=self.buscador_soluciones(),
            output_file='informe_soluciones_cerebras.md'
        )

    @crew
    def crew(self) -> Crew:
        """
        Crea y configura el Crew de soporte.
        """
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)

def run():
    """
    SCRIPT PARA PRUEBAS CON CEREBRAS: Lee una incidencia desde un fichero y pone
    en marcha el crew para analizarla usando la API de Cerebras.
    """
    try:
        with open('incidencia.txt', 'r', encoding='utf-8') as file:
            incidencia_texto = file.read()
    except FileNotFoundError:
        print("Error: No se encontró el fichero 'incidencia.txt' en la carpeta 'CrewAi'.")
        sys.exit(1)

    inputs = {
        'incidencia': incidencia_texto,
        'cat': "Redes, Hardware, Software, Cuentas de usuario, Permisos",
        'url_a_verificar': 'google.com'
    }

    SoporteIncidenciasCrewCerebras().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()