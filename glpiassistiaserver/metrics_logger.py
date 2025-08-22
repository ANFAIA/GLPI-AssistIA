import os
import csv
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import time

@dataclass
class CrewMetrics:
    """Clase para almacenar métricas de ejecución del crew."""
    ticket_id: str
    provider: str  # ollama, cerebras, groq
    model: str
    client_frustration: str
    total_tokens: int
    tools_used: List[str]
    agents_used: List[str]
    processing_time: float  # en segundos
    timestamp: str
    success: bool
    error_message: Optional[str] = None

class MetricsLogger:
    """Sistema de logging de métricas para el crew de GLPI, enfocado en CSV."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.csv_file = os.path.join(log_dir, "crew_metrics.csv")
        
        # Crear directorio de logs si no existe
        os.makedirs(log_dir, exist_ok=True)
        
        # Inicializar archivo CSV si no existe
        self._init_csv_file()
    
    def _init_csv_file(self):
        """Inicializa el archivo CSV con headers si no existe."""
        if not os.path.exists(self.csv_file):
            headers = [
                'timestamp', 'ticket_id', 'provider', 'model', 
                'client_frustration', 'total_tokens', 'tools_used', 
                'agents_used', 'processing_time', 'success', 'error_message'
            ]
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def log_metrics(self, metrics: CrewMetrics):
        """Registra las métricas en formato CSV y las muestra en pantalla."""
        try:
            # Log a consola
            self._print_to_console(metrics)
            
            # Log a CSV
            self._log_to_csv(metrics)
            
        except Exception as e:
            print(f"Error al registrar métricas: {e}")
    
    def _print_to_console(self, metrics: CrewMetrics):
        """Muestra métricas en la consola."""
        status = "ÉXITO" if metrics.success else "ERROR"
        
        log_message = f"""
{'='*50}
{status} - EJECUCIÓN CREW COMPLETADA
{'='*50}
ID Ticket: {metrics.ticket_id}
Proveedor: {metrics.provider}
Modelo: {metrics.model}
Frustración Cliente: {metrics.client_frustration}
Tokens Consumidos: {metrics.total_tokens:,}
Herramientas Usadas: {', '.join(metrics.tools_used)}
Agentes Empleados: {', '.join(metrics.agents_used)}
Tiempo de Procesamiento: {metrics.processing_time:.2f}s
Timestamp: {metrics.timestamp}
"""
        
        if not metrics.success and metrics.error_message:
            log_message += f"Error: {metrics.error_message}\n"
        
        log_message += "=" * 50
        
        print(log_message)
    
    def _log_to_csv(self, metrics: CrewMetrics):
        """Registra métricas en archivo CSV."""
        row = [
            metrics.timestamp,
            metrics.ticket_id,
            metrics.provider,
            metrics.model,
            metrics.client_frustration,
            metrics.total_tokens,
            '|'.join(metrics.tools_used), 
            '|'.join(metrics.agents_used), # <-- ¡Corregido aquí!
            metrics.processing_time,
            metrics.success,
            metrics.error_message or ''
        ]
        
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    
# Instancia global del logger
metrics_logger = MetricsLogger()

def log_crew_execution(
    ticket_id: str,
    provider: str,
    model: str,
    client_frustration: str,
    total_tokens: int,
    tools_used: List[str],
    agents_used: List[str],
    processing_time: float,
    success: bool = True,
    error_message: Optional[str] = None
):
    """Función helper para registrar métricas de ejecución del crew."""
    metrics = CrewMetrics(
        ticket_id=str(ticket_id),
        provider=provider,
        model=model,
        client_frustration=client_frustration,
        total_tokens=total_tokens,
        tools_used=tools_used,
        agents_used=agents_used,
        processing_time=processing_time,
        timestamp=datetime.now().isoformat(),
        success=success,
        error_message=error_message
    )
    
    metrics_logger.log_metrics(metrics)