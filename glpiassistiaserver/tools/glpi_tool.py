from crewai.tools import tool
from typing import Any, Dict
import json
import traceback

from .mcp_tools.glpi_handler import (
    GlpiError as _GlpiError,
    get_ticket_by_number as _get_ticket_by_number,
    search_similar_tickets as _search_similar_tickets,
    post_private_note_for_agent as _post_private_note_for_agent,
)

try:
    from fastapi import APIRouter, HTTPException, Query
    from pydantic import BaseModel, Field, conint
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False


@tool("glpi_tool")
def glpi_tool(payload: dict) -> str:
    """
    Interactúa con GLPI a través de la capa MCP (glpi_handler) mejorada.

    Actions soportadas:
      - "search_similar": Busca tickets similares usando algoritmos avanzados
        { "title": str, "content"?: str, "top_k"?: int<=20 }
      - "post_private_note": Envía una nota privada a un ticket
        { "ticket_id": int, "text": str }
      - "ticket_by_number": Busca un ticket por número/nombre
        { "number": str }

    Returns:
      JSON string con formato:
      - {"ok": true, ...} en caso de éxito
      - {"ok": false, "error": "mensaje"} en caso de error
    """
    try:
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError as e:
                return json.dumps({
                    "ok": False, 
                    "error": f"Formato JSON inválido: {str(e)}"
                }, ensure_ascii=False)
        
        if not isinstance(payload, dict):
            return json.dumps({
                "ok": False,
                "error": "El payload debe ser un diccionario"
            }, ensure_ascii=False)
        
        action = payload.get("action")
        if not action:
            return json.dumps({
                "ok": False,
                "error": "Falta el campo 'action' en el payload"
            }, ensure_ascii=False)

        # Procesar según la acción solicitada
        if action == "search_similar":
            return _handle_search_similar(payload)
        elif action == "post_private_note":
            return _handle_post_private_note(payload)
        elif action == "ticket_by_number":
            return _handle_ticket_by_number(payload)
        else:
            return json.dumps({
                "ok": False, 
                "error": f"Acción no reconocida: '{action}'. Acciones válidas: search_similar, post_private_note, ticket_by_number"
            }, ensure_ascii=False)

    except _GlpiError as e:
        return json.dumps({
            "ok": False, 
            "error": f"Error de GLPI: {str(e)}"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "ok": False, 
            "error": f"Error inesperado en glpi_tool: {e.__class__.__name__}: {str(e)}"
        }, ensure_ascii=False)


def _handle_search_similar(payload: Dict[str, Any]) -> str:
    """Maneja la búsqueda de tickets similares."""
    try:
        title = payload.get("title", "").strip()
        content = payload.get("content", "").strip()
        top_k = int(payload.get("top_k", 5))
        
        if not title and not content:
            return json.dumps({
                "ok": False,
                "error": "Se requiere al menos 'title' o 'content' para la búsqueda"
            }, ensure_ascii=False)
        
        if top_k < 1 or top_k > 20:
            return json.dumps({
                "ok": False,
                "error": "top_k debe estar entre 1 y 20"
            }, ensure_ascii=False)
        
        results = _search_similar_tickets(title, content, top_k)
        
        formatted_results = []
        for ticket, score in results:
            formatted_results.append({
                "ticket": {
                    "id": ticket.get("id"),
                    "name": ticket.get("name", ""),
                    "content": ticket.get("content", "")[:200] + "..." if len(ticket.get("content", "")) > 200 else ticket.get("content", ""),
                    "date": ticket.get("date", ""),
                    "date_mod": ticket.get("date_mod", "")
                },
                "similarity_score": round(score, 4)
            })
        
        return json.dumps({
            "ok": True, 
            "items": formatted_results,
            "total_found": len(formatted_results),
            "search_terms": {
                "title": title,
                "content": content[:100] + "..." if len(content) > 100 else content
            }
        }, ensure_ascii=False)
        
    except ValueError as e:
        return json.dumps({
            "ok": False,
            "error": f"Error en parámetros de búsqueda: {str(e)}"
        }, ensure_ascii=False)


def _handle_post_private_note(payload: Dict[str, Any]) -> str:
    """Maneja el envío de notas privadas."""
    try:
        ticket_id_raw = payload.get("ticket_id")
        text = payload.get("text", "").strip()
        
        if ticket_id_raw is None:
            return json.dumps({
                "ok": False,
                "error": "Campo 'ticket_id' requerido"
            }, ensure_ascii=False)
        
        try:
            ticket_id = int(ticket_id_raw)
            if ticket_id <= 0:
                raise ValueError("ID debe ser positivo")
        except (ValueError, TypeError):
            return json.dumps({
                "ok": False,
                "error": f"ticket_id debe ser un número entero positivo. Recibido: {ticket_id_raw}"
            }, ensure_ascii=False)
        
        if not text:
            return json.dumps({
                "ok": False,
                "error": "Campo 'text' requerido y no puede estar vacío"
            }, ensure_ascii=False)
        
        if text in ["context['output']", "{{output}}", "[CONTENIDO DEL INFORME ANTERIOR]"]:
            return json.dumps({
                "ok": False,
                "error": "El texto contiene un placeholder en lugar del contenido real. Verifica que el contexto se esté pasando correctamente."
            }, ensure_ascii=False)
        
        if len(text) > 65535:
            text = text[:65535] + "\n\n[Texto truncado por límite de longitud]"
        
        result = _post_private_note_for_agent(ticket_id, text)
        
        return json.dumps({
            "ok": True,
            "message": "Nota privada publicada correctamente en GLPI",
            "ticket_id": ticket_id,
            "note_length": len(text),
            "glpi_response": result
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "ok": False,
            "error": f"Error al enviar nota privada: {str(e)}"
        }, ensure_ascii=False)


def _handle_ticket_by_number(payload: Dict[str, Any]) -> str:
    """Maneja la búsqueda de tickets por número."""
    try:
        number = payload.get("number", "").strip()
        
        if not number:
            return json.dumps({
                "ok": False,
                "error": "Campo 'number' requerido y no puede estar vacío"
            }, ensure_ascii=False)
        
        ticket = _get_ticket_by_number(str(number))
        
        if ticket:
            formatted_ticket = {
                "id": ticket.get("id"),
                "name": ticket.get("name", ""),
                "content": ticket.get("content", ""),
                "date": ticket.get("date", ""),
                "date_mod": ticket.get("date_mod", ""),
                "status": ticket.get("status", ""),
                "priority": ticket.get("priority", "")
            }
            
            return json.dumps({
                "ok": True,
                "found": True,
                "ticket": formatted_ticket,
                "search_number": number
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "ok": True,
                "found": False,
                "ticket": None,
                "search_number": number,
                "message": f"No se encontró ningún ticket con el número '{number}'"
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "ok": False,
            "error": f"Error al buscar ticket por número: {str(e)}"
        }, ensure_ascii=False)


if FASTAPI_AVAILABLE:
    router = APIRouter(prefix="/mcp/glpi", tags=["glpi-mcp"])

    class SimilarQuery(BaseModel):
        title: str = Field(..., min_length=1, description="Título del ticket base")
        content: str = Field("", description="Descripción/Contenido (opcional)")
        top_k: conint(ge=1, le=20) = Field(5, description="Número máximo de resultados")

    class NoteInput(BaseModel):
        ticket_id: int = Field(..., ge=1, description="ID del ticket")
        text: str = Field(..., min_length=1, max_length=65535, description="Texto de la nota")

    @router.get("/ticket_by_number")
    def glpi_http_ticket_by_number(number: str = Query(..., min_length=1)) -> Dict[str, Any]:
        """Endpoint HTTP: Busca un ticket por número/nombre."""
        try:
            ticket = _get_ticket_by_number(number)
            return {
                "found": ticket is not None,
                "ticket": ticket,
                "search_number": number
            }
        except _GlpiError as e:
            raise HTTPException(status_code=400, detail=f"Error de GLPI: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

    @router.post("/search_similar")
    def glpi_http_search_similar(payload: SimilarQuery) -> Dict[str, Any]:
        """Endpoint HTTP: Busca incidencias similares usando algoritmos avanzados."""
        try:
            results = _search_similar_tickets(payload.title, payload.content, payload.top_k)
            
            formatted_results = []
            for ticket, score in results:
                formatted_results.append({
                    "ticket": ticket,
                    "similarity_score": round(score, 4)
                })
            
            return {
                "items": formatted_results,
                "total_found": len(formatted_results),
                "search_terms": {
                    "title": payload.title,
                    "content": payload.content
                }
            }
        except _GlpiError as e:
            raise HTTPException(status_code=400, detail=f"Error de GLPI: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

    @router.post("/post_private_note")
    def glpi_http_post_private_note(payload: NoteInput) -> Dict[str, Any]:
        """Endpoint HTTP: Añade una nota privada a un ticket."""
        try:
            result = _post_private_note_for_agent(payload.ticket_id, payload.text)
            return {
                "ok": True,
                "message": "Nota privada publicada correctamente",
                "ticket_id": payload.ticket_id,
                "glpi_response": result
            }
        except _GlpiError as e:
            raise HTTPException(status_code=400, detail=f"Error de GLPI: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

    @router.get("/test_connection")
    def glpi_http_test_connection() -> Dict[str, Any]:
        """Endpoint HTTP: Prueba la conexión a GLPI."""
        try:
            from .mcp_tools.glpi_handler import _init_session, _kill_session
            
            session_token = _init_session()
            _kill_session(session_token)
            
            return {
                "ok": True,
                "message": "Conexión a GLPI exitosa",
                "session_created": True
            }
        except _GlpiError as e:
            raise HTTPException(status_code=400, detail=f"Error de conexión GLPI: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")