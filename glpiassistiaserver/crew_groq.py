#---------------------------------------------------
# Intento de implementación de Groq (API) - INCOMPLETA
#---------------------------------------------------

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from dotenv import load_dotenv

script_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(script_dir, '.env.groq')
load_dotenv(dotenv_path=dotenv_path)

from tools.ping_tool import ping_tool
from tools.wikijs_mcp_tool import wikijs_mcp_tool 

@CrewBase
class SoporteIncidenciasCrewGroq():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("La variable de entorno GROQ_API_KEY no está configurada. Por favor, añádela a tu fichero .env.groq")

        self.sentiment_analyst_llm = ChatGroq(
            api_key=groq_api_key,
            model="groq/llama-3.1-8b-instant" 
        )
        self.classifier_llm = ChatGroq(
            api_key=groq_api_key,
            model="groq/llama-3.1-8b-instant"
        )
        self.solution_finder_llm = ChatGroq(
            api_key=groq_api_key,
            model="groq/llama3-70b-8192"
        )

    @agent
    def analista_sentimiento(self) -> Agent:
        return Agent(config=self.agents_config['analista_sentimiento'], llm=self.sentiment_analyst_llm, verbose=True)

    @agent
    def clasificador_incidencias(self) -> Agent:
        return Agent(config=self.agents_config['clasificador_incidencias'], llm=self.classifier_llm, verbose=True)

    @agent
    def buscador_soluciones(self) -> Agent:
        return Agent(
            config=self.agents_config['buscador_soluciones'],
            llm=self.solution_finder_llm,
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
            output_file='informe_soluciones_groq.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)