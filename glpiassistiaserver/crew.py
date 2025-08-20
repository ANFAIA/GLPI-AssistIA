import os
import time
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_cerebras import ChatCerebras

from .tools.ping_tool import ping_tool
from .tools.wikijs_mcp_tool import wikijs_mcp_tool
from .tools.glpi_tool import glpi_tool

# Importar el sistema de logging de métricas
from .metrics_logger import log_crew_execution


class CrewExecutionTracker:
    """Clase para trackear la ejecución del crew y recopilar métricas."""
    
    def __init__(self):
        self.start_time = None
        self.tools_used = set()
        self.agents_used = set()
        self.client_frustration = "Normal"
        
    def start_tracking(self):
        """Inicia el tracking de la ejecución."""
        self.start_time = time.time()
        self.tools_used = set()
        self.agents_used = set()
    
    def track_agent_usage(self, agent_name: str):
        """Registra el uso de un agente."""
        self.agents_used.add(agent_name)
    
    def track_tool_usage(self, tool_name: str):
        """Registra el uso de una herramienta."""
        self.tools_used.add(tool_name)
    
    def set_client_frustration(self, frustration_level: str):
        """Establece el nivel de frustración del cliente."""
        self.client_frustration = frustration_level
    
    def get_execution_time(self) -> float:
        """Calcula el tiempo de ejecución en segundos."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def get_tools_list(self) -> List[str]:
        """Devuelve la lista de herramientas utilizadas."""
        return list(self.tools_used)
    
    def get_agents_list(self) -> List[str]:
        """Devuelve la lista de agentes utilizados."""
        return list(self.agents_used)


@CrewBase
class SoporteIncidenciasCrew():
    """
    Crew para gestionar y resolver incidencias de soporte técnico usando Ollama
    con modelos especializados para cada tarea.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm, provider: str, model: str):
        """
        Inicializa el Crew definiendo los modelos LLM que se usarán para cada agente.
        """
        self.llm = llm
        self.provider = provider
        self.model = model
        self.execution_tracker = CrewExecutionTracker()

    @agent
    def analista_sentimiento(self) -> Agent:
        """
        Define el agente que analiza el sentimiento y la urgencia de la incidencia.
        """
        self.execution_tracker.track_agent_usage("analista_sentimiento")
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
        self.execution_tracker.track_agent_usage("clasificador_incidencias")
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
        self.execution_tracker.track_agent_usage("buscador_soluciones")
        
        # Trackear las herramientas que este agente puede usar
        for tool in [ping_tool, wikijs_mcp_tool, glpi_tool]:
            tool_name = getattr(tool, 'name', str(tool))
            self.execution_tracker.track_tool_usage(tool_name)
        
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
            output_file=f'informe_soluciones-{int(time.time() * 1000)}.md'
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
    
    def execute_with_tracking(self, inputs: dict) -> dict:
        """Ejecuta el crew con tracking completo de métricas."""
        ticket_id = inputs.get('id', 'unknown')
        
        # Iniciar tracking
        self.execution_tracker.start_tracking()
        
        try:
            print(f"\n Iniciando procesamiento del ticket #{ticket_id}")
            print(f" Proveedor: {self.provider}")
            print(f" Modelo: {self.model}")
            print("=" * 50)
            
            # Ejecutar el crew
            result = self.crew().kickoff(inputs=inputs)
            
            # Obtener información de tokens
            token_usage = getattr(result, 'token_usage', None)
            total_tokens = token_usage.total_tokens if token_usage else 0
            
            print(f"\n Uso de tokens: {total_tokens:,}")
            
            # Extraer el nivel de frustración del cliente desde el resultado del primer task
            frustration_level = "Normal"  # Default
            if hasattr(result, 'tasks_output') and result.tasks_output:
                # El primer task es el análisis de sentimiento
                sentiment_output = result.tasks_output[0].raw if result.tasks_output[0] else ""
                frustration_level = sentiment_output.strip() if sentiment_output else "Normal"
            
            self.execution_tracker.set_client_frustration(frustration_level)
            
            # Registrar métricas de éxito
            log_crew_execution(
                ticket_id=ticket_id,
                provider=self.provider,
                model=self.model,
                client_frustration=frustration_level,
                total_tokens=total_tokens,
                tools_used=self.execution_tracker.get_tools_list(),
                agents_used=self.execution_tracker.get_agents_list(),
                processing_time=self.execution_tracker.get_execution_time(),
                success=True
            )
            
            return result
            
        except Exception as e:
            # Registrar métricas de error
            log_crew_execution(
                ticket_id=ticket_id,
                provider=self.provider,
                model=self.model,
                client_frustration=self.execution_tracker.client_frustration,
                total_tokens=0,  # No hay tokens si falló
                tools_used=self.execution_tracker.get_tools_list(),
                agents_used=self.execution_tracker.get_agents_list(),
                processing_time=self.execution_tracker.get_execution_time(),
                success=False,
                error_message=str(e)
            )
            
            raise e


def build_crew():
    """Construye el crew con el proveedor de LLM apropiado."""
    provider = "unknown"
    model = "unknown"
    
    if "CEREBRAS_API_KEY" in os.environ:
        print("---EMPLEANDO API DE CEREBRAS---")
        provider = "cerebras"
        model = "cerebras/llama-3.3-70b"
        llm = ChatCerebras(
            api_key=os.environ["CEREBRAS_API_KEY"],
            model=model
        )
    elif "GROQ_API_KEY" in os.environ:
        print("---EMPLEANDO API DE GROQ---")
        provider = "groq"
        model = "groq/llama3-70b-8192"
        llm = ChatGroq(
            api_key=os.environ["GROQ_API_KEY"],
            model=model
        )
    else:
        print("---EMPLEANDO MODELOS LOCALES VÍA OLLAMA---")
        print("Se recomienda el uso de un proveedor mediante API para una mayor precisión y velocidad de respuesta. Puedes configurar tu API consultando las instrucciones disponibles en la documentación.")
        provider = "ollama"
        model = "ollama/qwen3"
        llm = ChatOllama(
            model=model,
            base_url="http://localhost:11434"
        )
    
    return SoporteIncidenciasCrew(llm, provider, model)