from crewai.tools import tool
from typing import Any, Dict
import json

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
    Interactúa con GLPI a través de la capa MCP (glpi_handler).

    Actions (payload["action"]):
      - "search_similar": { "title": str, "content"?: str, "top_k"?: int<=20 }
      - "post_private_note": { "ticket_id": int, "text": str }
      - "ticket_by_number": { "number": str }

    Devuelve JSON en string:
      - {"ok": true, ...} en éxito
      - {"ok": false, "error": "..."} en error
    """
    try:
        # Manejar diferentes formatos de entrada
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                return json.dumps({"ok": False, "error": "Formato JSON inválido"}, ensure_ascii=False)
        
        action = payload.get("action")

        if action == "search_similar":
            items = _search_similar_tickets(
                payload.get("title", ""),
                payload.get("content", ""),
                int(payload.get("top_k", 5)),
            )
            result = [{"ticket": t, "score": round(score, 4)} for (t, score) in items]
            return json.dumps({"ok": True, "items": result}, ensure_ascii=False)

        elif action == "post_private_note":
            try:
                tid = int(payload["ticket_id"])
                text = str(payload["text"])
                
                # Verificar que el texto no sea literal "context['output']"
                if text == "context['output']":
                    return json.dumps({
                        "ok": False, 
                        "error": "El texto contiene 'context[\"output\"]' literal en lugar del contenido real. Verifique el contexto."
                    }, ensure_ascii=False)
                
                res = _post_private_note_for_agent(tid, text)
                return json.dumps({
                    "ok": True, 
                    "message": "Nota privada publicada correctamente en GLPI",
                    "result": res
                }, ensure_ascii=False)
            except ValueError as e:
                return json.dumps({
                    "ok": False, 
                    "error": f"Error en ticket_id: debe ser un número entero válido. Recibido: {payload.get('ticket_id')}"
                }, ensure_ascii=False)

        elif action == "ticket_by_number":
            number = str(payload["number"])
            ticket = _get_ticket_by_number(number)
            return json.dumps(
                {"ok": True, "found": ticket is not None, "ticket": ticket},
                ensure_ascii=False,
            )

        else:
            return json.dumps(
                {"ok": False, "error": f"Acción no reconocida: {action}"},
                ensure_ascii=False,
            )

    except _GlpiError as e:
        return json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps(
            {"ok": False, "error": f"Error inesperado: {e.__class__.__name__}: {e}"},
            ensure_ascii=False,
        )


# --- Endpoints HTTP (opcionales) ---
# Usan prefijo y nombres únicos para evitar solapamiento con otros routers o funciones.
if FASTAPI_AVAILABLE:
    router = APIRouter(prefix="/mcp/glpi", tags=["glpi-mcp"])

    class SimilarQuery(BaseModel):
        title: str = Field(..., description="Título del ticket base")
        content: str = Field("", description="Descripción/Contenido (opcional)")
        top_k: conint(ge=1, le=20) = 5

    class NoteInput(BaseModel):
        ticket_id: int = Field(..., ge=1)
        text: str = Field(..., min_length=1, max_length=65535)

    @router.get("/ticket_by_number")
    def glpi_http_ticket_by_number(number: str = Query(..., min_length=1)) -> Dict[str, Any]:
        """MCP HTTP: Busca un ticket por número/nombre y devuelve el objeto GLPI."""
        try:
            ticket = _get_ticket_by_number(number)
            return {"found": ticket is not None, "ticket": ticket}
        except _GlpiError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")

    @router.post("/search_similar")
    def glpi_http_search_similar(payload: SimilarQuery) -> Dict[str, Any]:
        """MCP HTTP: Busca incidencias similares y devuelve top_k con score."""
        try:
            items = _search_similar_tickets(payload.title, payload.content, payload.top_k)
            result = [{"ticket": t, "score": round(score, 4)} for (t, score) in items]
            return {"items": result}
        except _GlpiError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")

    @router.post("/post_private_note")
    def glpi_http_post_private_note(payload: NoteInput) -> Dict[str, Any]:
        """MCP HTTP: Añade una nota privada con posibles soluciones."""
        try:
            res = _post_private_note_for_agent(payload.ticket_id, payload.text)
            return {"ok": True, "result": res}
        except _GlpiError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")
