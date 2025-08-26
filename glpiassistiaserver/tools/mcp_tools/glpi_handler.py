import os
import re
import requests
import json
import math
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
import unicodedata

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_URL = os.getenv("GLPI_API_URL")
APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
USER_TOKEN = os.getenv("GLPI_USER_TOKEN")
VERIFY_SSL = os.getenv("GLPI_VERIFY_SSL", "true").lower() in ("1", "true", "yes", "y")

class GlpiError(Exception):
    """Error de integración con GLPI."""

class TextSimilarity:
    """Clase para calcular similitud entre textos usando múltiples algoritmos."""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normaliza el texto para comparación."""
        if not text:
            return ""
        
        text = unicodedata.normalize('NFD', text.lower())
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> Set[str]:
        """Extrae palabras clave relevantes del texto."""
        if not text:
            return set()
        
        # Palabras vacías comunes en español
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 
            'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'una', 'del', 'los', 
            'las', 'si', 'me', 'ya', 'muy', 'mas', 'pero', 'como', 'ser', 'hay', 'este',
            'esta', 'esto', 'todos', 'todo', 'tiene', 'hacer', 'estar', 'can', 'cannot',
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
        }
        
        normalized = TextSimilarity.normalize_text(text)
        words = normalized.split()
        
        # Filtrar palabras cortas y stop words
        keywords = {w for w in words if len(w) >= min_length and w not in stop_words}
        
        return keywords
    
    @staticmethod
    def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        """Calcula similitud de Jaccard entre dos conjuntos."""
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def cosine_similarity(text1: str, text2: str) -> float:
        """Calcula similitud coseno usando TF-IDF simplificado."""
        if not text1 or not text2:
            return 0.0
        
        words1 = TextSimilarity.normalize_text(text1).split()
        words2 = TextSimilarity.normalize_text(text2).split()
        
        if not words1 or not words2:
            return 0.0
        
        # Crear vocabulario conjunto
        vocab = set(words1 + words2)
        
        # Calcular vectores TF
        vec1 = [words1.count(word) for word in vocab]
        vec2 = [words2.count(word) for word in vocab]
        
        # Calcular similitud coseno
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    @staticmethod
    def sequence_similarity(text1: str, text2: str) -> float:
        """Calcula similitud usando SequenceMatcher."""
        if not text1 or not text2:
            return 0.0
        
        norm1 = TextSimilarity.normalize_text(text1)
        norm2 = TextSimilarity.normalize_text(text2)
        
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    @staticmethod
    def combined_similarity(text1: str, text2: str, title1: str = "", title2: str = "") -> float:
        """Calcula similitud combinada usando múltiples algoritmos."""
        if not text1 or not text2:
            return 0.0
        
        # Pesos para cada algoritmo
        weights = {
            'sequence': 0.3,
            'cosine': 0.3,
            'jaccard': 0.25,
            'title_bonus': 0.15
        }
        
        # Similitud de secuencia
        seq_sim = TextSimilarity.sequence_similarity(text1, text2)
        
        # Similitud coseno
        cos_sim = TextSimilarity.cosine_similarity(text1, text2)
        
        # Similitud Jaccard con keywords
        keywords1 = TextSimilarity.extract_keywords(text1)
        keywords2 = TextSimilarity.extract_keywords(text2)
        jac_sim = TextSimilarity.jaccard_similarity(keywords1, keywords2)
        
        # Bonus por similitud en títulos
        title_sim = 0.0
        if title1 and title2:
            title_sim = TextSimilarity.sequence_similarity(title1, title2)
        
        # Combinar todas las métricas
        combined = (
            weights['sequence'] * seq_sim +
            weights['cosine'] * cos_sim +
            weights['jaccard'] * jac_sim +
            weights['title_bonus'] * title_sim
        )
        
        return min(1.0, combined)

def _parse_json_response(r: requests.Response):
    """Parsea JSON y elimina BOM si aparece al inicio de la respuesta."""
    try:
        # Usar el texto ya decodificado por requests y quitar BOM explícitamente
        text = r.text.lstrip('\ufeff')
        return json.loads(text)
    except Exception as e:
        raise GlpiError(f"Error al parsear respuesta JSON de GLPI: {e}")

def _check_cfg():
    """Verifica que las variables de configuración de GLPI estén definidas."""
    if not API_URL:
        raise GlpiError("GLPI_API_URL no está definida")
    if not APP_TOKEN:
        raise GlpiError("GLPI_APP_TOKEN no está definida")
    if not USER_TOKEN:
        raise GlpiError("GLPI_USER_TOKEN no está definida")

def _init_session() -> str:
    """Inicia sesión en GLPI y devuelve el token de sesión."""
    _check_cfg()
    headers = {"App-Token": APP_TOKEN, "Authorization": f"user_token {USER_TOKEN}"}
    
    try:
        r = requests.get(f"{API_URL}/initSession", headers=headers, verify=VERIFY_SSL, timeout=20)
        r.raise_for_status()
        
        response_data = _parse_json_response(r)
        token = response_data.get("session_token")
        
        if not token:
            raise GlpiError(f"GLPI no devolvió session_token. Respuesta: {response_data}")
        
        return token
    except requests.exceptions.RequestException as e:
        raise GlpiError(f"Error al conectar con GLPI: {e}")
    except ValueError as e:
        raise GlpiError(f"Error al parsear respuesta JSON de GLPI: {e}")

def _kill_session(session_token: str):
    """Cierra la sesión en GLPI."""
    try:
        headers = {"App-Token": APP_TOKEN, "Session-Token": session_token}
        requests.get(f"{API_URL}/killSession", headers=headers, verify=VERIFY_SSL, timeout=10)
    except Exception:
        pass

def _headers(session_token: str) -> Dict[str, str]:
    """Devuelve los headers necesarios para las peticiones a GLPI."""
    return {
        "App-Token": APP_TOKEN, 
        "Session-Token": session_token, 
        "Content-Type": "application/json"
    }

def _anonymize(text: str) -> str:
    """Anonimiza información sensible en el texto."""
    if not text:
        return ""
    
    # Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text, flags=re.IGNORECASE)
    
    # IPs
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', text)
    
    # Números largos (posibles teléfonos, IDs, etc.)
    text = re.sub(r'\b\d{5,}\b', '[NUM]', text)
    
    # URLs
    text = re.sub(r'https?://[^\s]+', '[URL]', text, flags=re.IGNORECASE)
    
    return text

def get_ticket_by_id(ticket_id: int, session_token: str) -> Dict:
    """Obtiene un ticket específico por su ID."""
    try:
        r = requests.get(
            f"{API_URL}/Ticket/{ticket_id}", 
            headers=_headers(session_token), 
            verify=VERIFY_SSL, 
            timeout=20
        )
        r.raise_for_status()
        
        ticket_data = _parse_json_response(r)
        
        # Verificar si el ticket existe
        if not ticket_data or (isinstance(ticket_data, list) and len(ticket_data) == 0):
            raise GlpiError(f"Ticket con ID {ticket_id} no encontrado")
        
        return ticket_data
        
    except requests.exceptions.RequestException as e:
        raise GlpiError(f"Error al obtener ticket {ticket_id}: {e}")

def get_ticket_by_number(ticket_number: str) -> Optional[Dict]:
    """Busca un ticket por 'número/nombre' y devuelve el objeto completo, o None si no hay coincidencias."""
    if not ticket_number or not str(ticket_number).strip():
        return None
    
    session_token = _init_session()
    try:
        # Buscar por nombre del ticket
        r = requests.get(
            f"{API_URL}/search/Ticket",
            headers=_headers(session_token),
            params={
                "criteria[0][field]": "1",           # name
                "criteria[0][searchtype]": "contains",
                "criteria[0][value]": str(ticket_number).strip(),
                "forcedisplay[0]": "2",              # name
                "forcedisplay[1]": "12",             # content
                "range": "0-1"                       # Solo necesitamos el primer resultado
            },
            verify=VERIFY_SSL,
            timeout=30
        )
        r.raise_for_status()
        
        data = _parse_json_response(r)
        
        if not data or data.get("totalcount", 0) == 0:
            return None
        
        # Obtener el ticket completo
        ticket_id = data['data'][0][0]
        return get_ticket_by_id(ticket_id, session_token)
        
    except requests.exceptions.RequestException as e:
        raise GlpiError(f"Error al buscar ticket por número '{ticket_number}': {e}")
    except (KeyError, IndexError) as e:
        raise GlpiError(f"Error al procesar respuesta de búsqueda: {e}")
    finally:
        _kill_session(session_token)

def get_all_tickets_for_similarity(session_token: str, limit: int = 100) -> List[Dict]:
    """Obtiene todos los tickets para análisis de similitud."""
    try:
        all_tickets = []
        start = 0
        batch_size = 50  # Procesar en lotes para evitar timeouts
        
        while len(all_tickets) < limit:
            r = requests.get(
                f"{API_URL}/search/Ticket",
                headers=_headers(session_token),
                params={
                    "criteria[0][field]": "12",      # content (para obtener tickets con contenido)
                    "criteria[0][searchtype]": "contains",
                    "criteria[0][value]": "*",       # Wildcard para obtener todos
                    "forcedisplay[0]": "1",          # id
                    "forcedisplay[1]": "2",          # name
                    "forcedisplay[2]": "12",         # content
                    "forcedisplay[3]": "15",         # date
                    "forcedisplay[4]": "19",         # date_mod
                    "range": f"{start}-{start + batch_size - 1}",
                    "order": "DESC",
                    "sort": "19"                     # Ordenar por fecha de modificación
                },
                verify=VERIFY_SSL,
                timeout=30
            )
            r.raise_for_status()
            
            data = _parse_json_response(r)
            
            if not data or data.get("totalcount", 0) == 0:
                break
            
            for row in data.get('data', []):
                if len(all_tickets) >= limit:
                    break
                
                try:
                    ticket_basic = {
                        'id': row[0],
                        'name': row[1] if len(row) > 1 else '',
                        'content': row[2] if len(row) > 2 else '',
                        'date': row[3] if len(row) > 3 else '',
                        'date_mod': row[4] if len(row) > 4 else ''
                    }
                    
                    if ticket_basic.get('name') or ticket_basic.get('content'):
                        all_tickets.append(ticket_basic)
                        
                except (IndexError, TypeError):
                    continue 
            
            # Si no hay más datos, terminar
            if len(data.get('data', [])) < batch_size:
                break
                
            start += batch_size
        
        return all_tickets
        
    except requests.exceptions.RequestException as e:
        raise GlpiError(f"Error al obtener tickets para similitud: {e}")

def search_similar_tickets(title: str, content: str = "", top_k: int = 5) -> List[Tuple[Dict, float]]:
    """
    Busca tickets similares usando algoritmos avanzados de similitud de texto.
    
    Args:
        title: Título del ticket de referencia
        content: Contenido del ticket de referencia
        top_k: Número máximo de resultados a devolver
    
    Returns:
        Lista de tuplas (ticket, score) ordenadas por similitud descendente
    """
    if not title and not content:
        return []
    
    # Validar y ajustar top_k
    top_k = max(1, min(top_k, 20))
    
    session_token = _init_session()
    try:
        # Obtener tickets para comparación
        all_tickets = get_all_tickets_for_similarity(session_token, limit=200)
        
        if not all_tickets:
            return []
        
        # Texto de referencia para comparar
        reference_text = f"{title} {content}".strip()
        reference_anon = _anonymize(reference_text)
        
        scored_tickets = []
        
        for ticket_basic in all_tickets:
            try:
                # Obtener ticket completo para análisis detallado
                full_ticket = get_ticket_by_id(ticket_basic['id'], session_token)
                
                # Texto candidato
                candidate_title = full_ticket.get('name', '')
                candidate_content = full_ticket.get('content', '')
                candidate_text = f"{candidate_title} {candidate_content}".strip()
                
                if not candidate_text:
                    continue
                
                candidate_anon = _anonymize(candidate_text)
                
                # Calcular similitud usando el algoritmo combinado
                similarity_score = TextSimilarity.combined_similarity(
                    reference_anon, 
                    candidate_anon,
                    _anonymize(title),
                    _anonymize(candidate_title)
                )
                
                # Solo incluir si tiene similitud mínima
                if similarity_score > 0.1:  # Umbral mínimo de similitud
                    scored_tickets.append((full_ticket, float(similarity_score)))
                    
            except Exception as e:
                print(f"Error procesando ticket {ticket_basic.get('id', 'unknown')}: {e}")
                continue
        
        # Ordenar por similitud descendente y devolver top_k
        scored_tickets.sort(key=lambda x: x[1], reverse=True)
        return scored_tickets[:top_k]
        
    except Exception as e:
        raise GlpiError(f"Error en búsqueda de similitud: {e}")
    finally:
        _kill_session(session_token)

def post_private_note_for_agent(ticket_id: int, text: str) -> Dict:
    """Crea un followup privado en un ticket dado."""
    if not text or not text.strip():
        raise GlpiError("El texto de la nota no puede estar vacío.")
    
    if not isinstance(ticket_id, int) or ticket_id <= 0:
        raise GlpiError(f"ticket_id debe ser un entero positivo. Recibido: {ticket_id}")
    
    session_token = _init_session()
    try:
        try:
            get_ticket_by_id(ticket_id, session_token)
        except GlpiError as e:
            raise GlpiError(f"No se puede agregar nota al ticket {ticket_id}: {e}")
        
        payload = {
            "input": {
                "tickets_id": ticket_id, 
                "is_private": 1, 
                "content": text.strip()
            }
        }
        
        url = f"{API_URL.rstrip('/')}/Ticket/{ticket_id}/TicketFollowup"
        
        r = requests.post(
            url,
            headers=_headers(session_token),
            json=payload,
            verify=VERIFY_SSL,
            timeout=30
        )
        r.raise_for_status()
        
        response_data = _parse_json_response(r)
        
        if not response_data:
            raise GlpiError("GLPI devolvió respuesta vacía al crear followup")
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        raise GlpiError(f"Error al crear nota privada en ticket {ticket_id}: {e}")
    finally:
        _kill_session(session_token)

# Funciones de prueba y depuración
def test_similarity_algorithms():
    """Función para probar los algoritmos de similitud."""
    test_cases = [
        {
            "text1": "El servidor no responde y no puedo conectarme",
            "text2": "Servidor sin respuesta, conexión imposible",
            "expected_high": True
        },
        {
            "text1": "Problema con la impresora HP LaserJet",
            "text2": "La impresora HP LaserJet no funciona",
            "expected_high": True
        },
        {
            "text1": "Error de red en el equipo",
            "text2": "No puedo imprimir documentos",
            "expected_high": False
        }
    ]
    
    print("=== Pruebas de Algoritmos de Similitud ===")
    
    for i, case in enumerate(test_cases, 1):
        similarity = TextSimilarity.combined_similarity(case["text1"], case["text2"])
        expected = "Alta" if case["expected_high"] else "Baja"
        result = "✓" if (similarity > 0.5) == case["expected_high"] else "✗"
        
        print(f"Caso {i}: {result}")
        print(f"  Texto 1: {case['text1']}")
        print(f"  Texto 2: {case['text2']}")
        print(f"  Similitud: {similarity:.3f} (Esperada: {expected})")
        print()

if __name__ == "__main__":
    test_similarity_algorithms()