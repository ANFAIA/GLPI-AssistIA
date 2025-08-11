import os
from time import time

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatOllama
from langchain_cerebras import ChatCerebras

from tools.ping_tool import ping_tool
from tools.wikijs_mcp_tool import wikijs_mcp_tool

@CrewBase
class SoporteIncidenciasCrew():
    """
    Crew para gestionar y resolver incidencias de soporte técnico usando Ollama
    con modelos especializados para cada tarea.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm):
        """
        Inicializa el Crew definiendo los modelos LLM de Ollama que se usarán para cada agente.
        """
        self.llm = llm

    @agent
    def analista_sentimiento(self) -> Agent:
        """
        Define el agente que analiza el sentimiento y la urgencia de la incidencia.
        """
        return Agent(
            config=self.agents_config['analista_sentimiento'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def clasificador_incidencias(self) -> Agent:
        """
        Define el agente que clasifica la incidencia en una categoría técnica.
        """
        return Agent(
            config=self.agents_config['clasificador_incidencias'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def buscador_soluciones(self) -> Agent:
        """
        Define el agente que busca soluciones en la base de conocimiento.
        """
        return Agent(
            config=self.agents_config['buscador_soluciones'],
            llm=self.llm,
            # 2. Reemplazamos wikijs_tool por wikijs_mcp_tool
            tools=[ping_tool, wikijs_mcp_tool],
            verbose=True
        )

    @task
    def analizar_sentimiento_task(self) -> Task:
        """
        Define la tarea de análisis de sentimiento, asignada al agente correspondiente.
        """
        return Task(
            config=self.tasks_config['analizar_sentimiento_task'],
            agent=self.analista_sentimiento()
        )

    @task
    def clasificar_incidencia_task(self) -> Task:
        """
        Define la tarea de clasificación, asignada al agente clasificador.
        """
        return Task(
            config=self.tasks_config['clasificar_incidencia_task'],
            agent=self.clasificador_incidencias()
        )

    @task
    def buscar_soluciones_task(self) -> Task:
        """
        Define la tarea de búsqueda de soluciones y generación de un informe.
        """
        return Task(
            config=self.tasks_config['buscar_soluciones_task'],
            agent=self.buscador_soluciones(),
            output_file=f'informe_soluciones-{int(time() * 1000)}.md'
        )

    @crew
    def crew(self) -> Crew:
        """Crea y configura el Crew de soporte de incidencias."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


def build_crew():
    if "CEREBRAS_API_KEY" in os.environ:
        llm = ChatCerebras(
            api_key=os.environ["CEREBRAS_API_KEY"],
            model="cerebras/llama-3.3-70b"
        )
    else:
        llm = ChatOllama(
            model="ollama/qwen3",
            base_url="http://localhost:11434"
        )

    return SoporteIncidenciasCrew(llm)
