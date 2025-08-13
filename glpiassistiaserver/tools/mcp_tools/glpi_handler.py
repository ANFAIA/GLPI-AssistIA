import os
import re
import requests
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional

API_URL = os.getenv("GLPI_API_URL")
APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
USER_TOKEN = os.getenv("GLPI_USER_TOKEN")
VERIFY_SSL = os.getenv("GLPI_VERIFY_SSL", "true").lower() in ("1", "true", "yes", "y")

class GlpiError(Exception):
    """Error de integración con GLPI."""

def _init_session() -> str:
    _check_cfg()
    headers = {"App-Token": APP_TOKEN, "Authorization": f"user_token {USER_TOKEN}"}
    r = requests.get(f"{API_URL}/initSession", headers=headers, verify=VERIFY_SSL, timeout=20)
    r.raise_for_status()
    token = r.json().get("session_token")
    if not token:
        raise GlpiError("GLPI no devolvió session_token")
    return token

def _kill_session(session_token: str):
    try:
        headers = {"App-Token": APP_TOKEN, "Session-Token": session_token}
        requests.get(f"{API_URL}/killSession", headers=headers, verify=VERIFY_SSL, timeout=10)
    except Exception:
        pass

def _headers(session_token: str) -> Dict[str, str]:
    return {"App-Token": APP_TOKEN, "Session-Token": session_token, "Content-Type": "application/json"}

def _anonymize(text: str) -> str:
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', text)
    text = re.sub(r'\b\d{5,}\b', '[NUM]', text)
    return text

def get_ticket_by_id(ticket_id: int, session_token: str) -> Dict:
    r = requests.get(f"{API_URL}/Ticket/{ticket_id}", headers=_headers(session_token), verify=VERIFY_SSL, timeout=20)
    r.raise_for_status()
    return r.json()

def get_ticket_by_number(ticket_number: str) -> Optional[Dict]:
    """Busca un ticket por 'número/nombre' y devuelve el objeto completo, o None si no hay coincidencias."""
    session_token = _init_session()
    try:
        r = requests.get(
            f"{API_URL}/search/Ticket",
            headers=_headers(session_token),
            params={
                "criteria[0][field]": "1",           # name
                "criteria[0][searchtype]": "contains",
                "criteria[0][value]": str(ticket_number),
                "forcedisplay[0]": "2",              # name
                "forcedisplay[1]": "12"              # content
            },
            verify=VERIFY_SSL,
            timeout=30
        )
        r.raise_for_status()
        data = r.json()
        if data.get("totalcount", 0) == 0:
            return None
        ticket_id = data['data'][0][0]
        return get_ticket_by_id(ticket_id, session_token)
    finally:
        _kill_session(session_token)

def search_similar_tickets(title: str, content: str = "", top_k: int = 5) -> List[Tuple[Dict, float]]:
    """Devuelve [(ticket, score)] con incidencias similares al título+contenido dado."""
    session_token = _init_session()
    try:
        # keywords básicas (palabras de >=4 chars)
        import re as _re
        keywords = ' '.join(_re.findall(r'\w{4,}', title)[:5]) or title
        r = requests.get(
            f"{API_URL}/search/Ticket",
            headers=_headers(session_token),
            params={
                "criteria[0][field]": "1",
                "criteria[0][searchtype]": "contains",
                "criteria[0][value]": keywords,
                "forcedisplay[0]": "2",
                "forcedisplay[1]": "12"
            },
            verify=VERIFY_SSL,
            timeout=30
        )
        r.raise_for_status()
        results = r.json().get('data', [])
        scored = []
        base = _anonymize(f"{title} {content}")
        for row in results:
            tid = row[0]
            ticket = get_ticket_by_id(tid, session_token)
            cand = _anonymize(f"{ticket.get('name','')} {ticket.get('content','')}")
            score = SequenceMatcher(None, base, cand).ratio()
            scored.append((ticket, float(score)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:max(1, min(top_k, 20))]
    finally:
        _kill_session(session_token)

def post_private_note_for_agent(ticket_id: int, text: str) -> Dict:
    """Crea un followup privado en un ticket dado."""
    if not text or not text.strip():
        raise GlpiError("El texto de la nota no puede estar vacío.")
    session_token = _init_session()
    try:
        payload = {"input": {"tickets_id": ticket_id, "is_private": 1, "content": text}}
        r = requests.post(
            f"{API_URL}/Ticket/{ticket_id}/TicketFollowup",
            headers=_headers(session_token),
            json=payload,
            verify=VERIFY_SSL,
            timeout=30
        )
        r.raise_for_status()
        return r.json()
    finally:
        _kill_session(session_token)
