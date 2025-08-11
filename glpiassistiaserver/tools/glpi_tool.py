import requests
import re
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional

# -------------------------
# Configuración de conexión (Cambiar por datos)
# -------------------------
API_URL = "https://tu.glpi/api"
APP_TOKEN = "tu_app_token"
USER_TOKEN = "tu_user_token"
VERIFY_SSL = True


# -------------------------
# Conexión y cabeceras
# -------------------------
def _init_session() -> str:
    headers = {
        'App-Token': APP_TOKEN,
        'Authorization': f'user_token {USER_TOKEN}'
    }
    r = requests.get(f"{API_URL.rstrip('/')}/initSession", headers=headers, verify=VERIFY_SSL)
    r.raise_for_status()
    return r.json().get('session_token')


def _kill_session(session_token: str):
    headers = {
        'App-Token': APP_TOKEN,
        'Session-Token': session_token
    }
    requests.get(f"{API_URL.rstrip('/')}/killSession", headers=headers, verify=VERIFY_SSL)


def _headers(session_token: str) -> Dict[str, str]:
    return {
        'App-Token': APP_TOKEN,
        'Session-Token': session_token,
        'Content-Type': 'application/json'
    }


# -------------------------
# Funciones GLPI
# -------------------------
def get_ticket_by_number(ticket_number: str) -> Optional[Dict]:
    """Tool: Busca un ticket por número y devuelve su información completa."""
    session_token = _init_session()
    try:
        r = requests.get(
            f"{API_URL.rstrip('/')}/search/Ticket",
            headers=_headers(session_token),
            params={
                "criteria[0][field]": "1",  # name
                "criteria[0][searchtype]": "contains",
                "criteria[0][value]": str(ticket_number),
                "forcedisplay[0]": "2",   # name
                "forcedisplay[1]": "12"   # content
            },
            verify=VERIFY_SSL
        )
        r.raise_for_status()
        data = r.json()
        if data.get("totalcount", 0) == 0:
            return None
        ticket_id = data['data'][0][0]
        return get_ticket_by_id(ticket_id, session_token)
    finally:
        _kill_session(session_token)


def get_ticket_by_id(ticket_id: int, session_token: str) -> Dict:
    r = requests.get(f"{API_URL.rstrip('/')}/Ticket/{ticket_id}", headers=_headers(session_token), verify=VERIFY_SSL)
    r.raise_for_status()
    return r.json()


def search_similar_tickets(title: str, content: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
    """Tool: Busca tickets con contenido similar."""
    session_token = _init_session()
    try:
        keywords = ' '.join(re.findall(r'\w{4,}', title)[:5]) or title
        r = requests.get(
            f"{API_URL.rstrip('/')}/search/Ticket",
            headers=_headers(session_token),
            params={
                "criteria[0][field]": "1",
                "criteria[0][searchtype]": "contains",
                "criteria[0][value]": keywords,
                "forcedisplay[0]": "2",
                "forcedisplay[1]": "12"
            },
            verify=VERIFY_SSL
        )
        r.raise_for_status()
        results = r.json().get('data', [])
        scored = []
        for row in results:
            tid = row[0]
            ticket = get_ticket_by_id(tid, session_token)
            score = SequenceMatcher(
                None,
                _anonymize(title + content),
                _anonymize(ticket.get('name', '') + ticket.get('content', ''))
            ).ratio()
            scored.append((ticket, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
    finally:
        _kill_session(session_token)


def post_private_note_for_agent(ticket_id: int, text: str) -> Dict:
    """Tool: Publica una nota privada (followup) en un ticket."""
    session_token = _init_session()
    try:
        payload = {
            "input": {
                "tickets_id": ticket_id,
                "is_private": 1,
                "content": text
            }
        }
        r = requests.post(
            f"{API_URL.rstrip('/')}/Ticket/{ticket_id}/TicketFollowup",
            headers=_headers(session_token),
            json=payload,
            verify=VERIFY_SSL
        )
        r.raise_for_status()
        return r.json()
    finally:
        _kill_session(session_token)


# -------------------------
# Eliminación de datos sensibles
# -------------------------
def _anonymize(text: str) -> str:
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', text)
    text = re.sub(r'\b\d{5,}\b', '[NUM]', text)
    return text
