#---------------------------------------------------
# Implementación de Cerebras (API)
#---------------------------------------------------
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms.litellm import LiteLLM

script_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(script_dir, '.env.cerebras')
load_dotenv(dotenv_path=dotenv_path)

cerebras_api_key = "API_KEY"

from tools.ping_tool import ping_tool
from tools.wikijs_mcp_tool import wikijs_mcp_tool

@CrewBase
class SoporteIncidenciasCrewCerebras():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.llm = LiteLLM(
            model="llama-3.3-70b",
            api_key=os.environ.get("CEREBRAS_API_KEY"),
            llm_provider="cerebras"
        )

    @agent
    def analista_sentimiento(self) -> Agent:
        return Agent(config=self.agents_config['analista_sentimiento'], llm=self.llm, verbose=True)

    @agent
    def clasificador_incidencias(self) -> Agent:
        return Agent(config=self.agents_config['clasificador_incidencias'], llm=self.llm, verbose=True)

    @agent
    def buscador_soluciones(self) -> Agent:
        return Agent(
            config=self.agents_config['buscador_soluciones'],
            llm=self.llm,
            tools=[ping_tool, wikijs_mcp_tool],
            verbose=True
        )

    @task
    def analizar_sentimiento_task(self) -> Task:
        return Task(config=self.tasks_config['analizar_sentimiento_task'], agent=self.analista_sentimiento())

    @task
    def clasificar_incidencia_task(self) -> Task:
        return Task(config=self.tasks_config['clasificar_incidencia_task'], agent=self.clasificador_incidencias())

    @task
    def buscar_soluciones_task(self) -> Task:
        return Task(
            config=self.tasks_config['buscar_soluciones_task'],
            agent=self.buscador_soluciones(),
            output_file='informe_soluciones_cerebras.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True) 