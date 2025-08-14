import os
from time import time

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_cerebras import ChatCerebras

from .tools.ping_tool import ping_tool
from .tools.wikijs_mcp_tool import wikijs_mcp_tool
from .tools.glpi_tool import glpi_tool


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
            tools=[ping_tool, wikijs_mcp_tool, glpi_tool],
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
    
    @task
    def publicar_en_glpi_task(self) -> Task:
        return Task(
            description=(
                "Utiliza la herramienta glpi_tool para publicar el informe técnico como una nota privada en GLPI.\n"
                "- action: 'post_private_note'\n"
                "- ticket_id: {{id}}\n"
                "- text: El contenido del informe generado por el agente anterior\n\n"
                "**IMPORTANTE**: Debes usar el contenido real del informe generado anteriormente. El contexto contiene el resultado de la tarea anterior.\n\n"
                "**INTERPRETACIÓN DE RESPUESTA**: Si la herramienta devuelve {\"ok\": true, \"message\": \"Nota privada publicada correctamente en GLPI\"}, significa que la operación fue exitosa.\n\n"
                "Formato obligatorio:\n"
                "Thought: Publicaré el informe generado\n"
                "Action: glpi_tool\n"
                "Action Input: {\n"
                "  \"payload\": {\n"
                "    \"action\": \"post_private_note\",\n"
                "    \"ticket_id\": {{id}},\n"
                "    \"text\": \"[CONTENIDO DEL INFORME ANTERIOR]\"\n"
                "  }\n"
                "}"
            ),
            expected_output="Nota privada publicada correctamente en GLPI con el contenido del informe técnico",
            agent=self.buscador_soluciones(),
            tools=[glpi_tool],
            context=[self.buscar_soluciones_task()],
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        """Crea y configura el Crew de soporte de incidencias."""
        return Crew(
            agents=self.agents,
            tasks=[
            self.analizar_sentimiento_task(),
            self.clasificar_incidencia_task(),
            self.buscar_soluciones_task(),
            self.publicar_en_glpi_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )

def build_crew():
    if "CEREBRAS_API_KEY" in os.environ:
        print("---EMPLEANDO API DE CEREBRAS---")
        llm = ChatCerebras(
            api_key=os.environ["CEREBRAS_API_KEY"],
            model="cerebras/llama-3.3-70b"
        )
    elif "GROQ_API_KEY" in os.environ:
        print("---EMPLEANDO API DE GROQ---")
        llm = ChatGroq(
            api_key=os.environ["GROQ_API_KEY"],
            model= "groq/llama3-70b-8192"
        )
    else:
        print("---EMPLEANDO MODELOS LOCALES VÍA OLLAMA---")
        print("Se recomienda el uso de un proveedor mediante API para una mayor precisión y velocidad de respuesta. Puedes configurar tu API consultando las instrucciones disponibles en la documentación.")
        llm = ChatOllama(
            model="ollama/qwen3",
            base_url="http://localhost:11434"
        )
        

    return SoporteIncidenciasCrew(llm)