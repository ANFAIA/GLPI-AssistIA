class GLPIClient:
    
    def __init__(self, url=None, app_token=None, user_token=None):
        """
        Inicializa el cliente GLPI con parámetros de configuración.
        En este prototipo, los parámetros se aceptan pero no se utilizan.
        """
        self.url = url
        self.app_token = app_token
        self.user_token = user_token
        print(f"Cliente GLPI inicializado - URL: {url}")
    
    def get_ticket_full_content(self, ticket_id: int) -> str:
        """
        Obtiene el contenido completo de un ticket.
        En este prototipo, devuelve un ticket de ejemplo codificado internamente.
        
        Args:
            ticket_id (int): ID del ticket (no utilizado en la simulación)
            
        Returns:
            str: Contenido completo del ticket de ejemplo
        """
        print(f"Obteniendo contenido del ticket #{ticket_id} (simulado)")
        
        # Ticket de ejemplo - Realizado por una IA generativa y revisado por un humano
        ticket_content = f"""
=== TICKET #{ticket_id} - PROBLEMA DE CONECTIVIDAD DE RED ===

TÍTULO: Usuario no puede acceder a la red corporativa desde su portátil

DESCRIPCIÓN INICIAL:
El usuario Juan Pérez (juan.perez@empresa.com) reporta que desde esta mañana no puede conectarse a la red corporativa desde su portátil Dell Latitude 5520. El equipo muestra el mensaje "No se puede conectar a esta red" cuando intenta conectarse al WiFi de la oficina. El usuario confirma que la contraseña es correcta y que otros dispositivos en la misma ubicación funcionan normalmente.

INFORMACIÓN TÉCNICA:
- Modelo: Dell Latitude 5520
- Sistema Operativo: Windows 11 Pro
- Adaptador WiFi: Intel Wi-Fi 6 AX201
- Última actualización: Hace 2 días

SEGUIMIENTO #1 - Técnico: María González (09:30 AM):
He verificado que el usuario está en la lista de dispositivos autorizados en el controlador de acceso. El problema parece estar relacionado con el certificado de autenticación. He solicitado al usuario que reinicie el servicio de Windows "Servicio de configuración automática de redes inalámbricas" y que elimine la red WiFi de su lista de redes conocidas para volver a agregarla.

SEGUIMIENTO #2 - Técnico: Carlos Rodríguez (11:15 AM):
El usuario ha seguido las instrucciones pero el problema persiste. He verificado que el certificado RADIUS en el equipo no está actualizado. He descargado e instalado el nuevo certificado desde el portal de IT. También he actualizado los drivers del adaptador WiFi a la versión más reciente disponible en el sitio web de Dell.

SEGUIMIENTO #3 - Técnico: Ana Martínez (02:45 PM):
Después de la actualización del certificado y drivers, el usuario sigue sin poder conectarse. He realizado un diagnóstico completo del adaptador de red y detecté que hay un conflicto con el software antivirus corporativo. He agregado una excepción para el proceso de autenticación WiFi en el antivirus. El usuario debe reiniciar el equipo para que los cambios surtan efecto.

ESTADO ACTUAL: En espera de confirmación del usuario después del reinicio.
PRIORIDAD: Media
CATEGORÍA: Redes / WiFi
ASIGNADO A: Equipo de Soporte de Redes
"""
        
        return ticket_content 