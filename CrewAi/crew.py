# src/my_project/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatOllama

@CrewBase
class SoporteIncidenciasCrew():
    """
    Crew para gestionar y resolver incidencias de soporte técnico usando Ollama 
    con el modelo deepseek-coder.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        """
        Inicializa el Crew definiendo el modelo LLM de Ollama que se usará.
        """
        self.ollama_llm = ChatOllama(
            model = "deepseek-coder",
            base_url = "http://localhost:11434" # URL estándar de Ollama
        )

    @agent
    def analista_sentimiento(self) -> Agent:
        """
        Define el agente que analiza el sentimiento y la urgencia de la incidencia.
        """
        return Agent(
            config=self.agents_config['analista_sentimiento'],
            llm=self.ollama_llm,  # Asigna el modelo Ollama al agente
            verbose=True
        )

    @agent
    def clasificador_incidencias(self) -> Agent:
        """
        Define el agente que clasifica la incidencia en una categoría técnica.
        """
        return Agent(
            config=self.agents_config['clasificador_incidencias'],
            llm=self.ollama_llm,  # Asigna el modelo Ollama al agente
            verbose=True
        )

    @agent
    def buscador_soluciones(self) -> Agent:
        """
        Define el agente que busca soluciones en la base de conocimiento.
        """
        return Agent(
            config=self.agents_config['buscador_soluciones'],
            llm=self.ollama_llm,  # Asigna el modelo Ollama al agente
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
            output_file='informe_deepseek.md' # Fichero de salida opcional
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