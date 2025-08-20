<?php

function plugin_glpiassistia_trigger_ia_on_ticket($ticket)
{
    if ($ticket->getType() !== 'Ticket') {
        return true;
    }

    $ticket_id = $ticket->getID();
    $title = isset($ticket->fields['name']) ? $ticket->fields['name'] : '';
    $content = isset($ticket->fields['content']) ? $ticket->fields['content'] : '';

    // Crear el payload en el formato solicitado
    $payload = [
        'id' => $ticket_id,
        'title' => $title,
        'description' => $content
    ];

    // Obtener la configuración del plugin
    $config = Config::getConfigurationValues('plugin:AssistIA');
    $server_url = isset($config['server_url']) && !empty($config['server_url'])
        ? rtrim($config['server_url'], '/')
        : null;

    if (!$server_url) {
        // Registrar error si no hay URL configurada
        Toolbox::logInFile('glpi_assistia', 
            "Error: URL del servidor AssistIA no configurada para el ticket ID: $ticket_id\n");
        return true;
    }

    // Preparar la petición HTTP
    $ch = curl_init($server_url);
    $json_payload = json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => 'POST',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Content-Length: ' . strlen($json_payload)
        ],
        CURLOPT_POSTFIELDS => $json_payload,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_SSL_VERIFYHOST => false
    ]);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curl_error = curl_error($ch);
    curl_close($ch);

    // Verificar si hubo errores
    if ($response === false || !empty($curl_error)) {
        $error_msg = "Error de conexión con el servidor AssistIA para el ticket ID: $ticket_id - " . 
                     ($curl_error ?: 'Error desconocido');
        Toolbox::logInFile('glpi_assistia', $error_msg . "\n");
        
        // Mostrar mensaje de error al usuario si está en interfaz web
        if (isset($_SESSION['glpiactiveprofile'])) {
            Session::addMessageAfterRedirect(
                'Error: No se pudo conectar con el servidor AssistIA. Verifique la configuración.',
                false,
                ERROR
            );
        }
        return true;
    }

    // Verificar código de respuesta HTTP
    if ($http_code < 200 || $http_code >= 300) {
        $error_msg = "Error del servidor AssistIA para el ticket ID: $ticket_id - " . 
                     "Código HTTP: $http_code - Respuesta: " . substr($response, 0, 500);
        Toolbox::logInFile('glpi_assistia', $error_msg . "\n");
        
        if (isset($_SESSION['glpiactiveprofile'])) {
            Session::addMessageAfterRedirect(
                "Error del servidor AssistIA (HTTP $http_code). Consulte los logs para más detalles.",
                false,
                ERROR
            );
        }
        return true;
    }

    // Log de éxito
    Toolbox::logInFile('glpi_assistia', 
        "Ticket ID: $ticket_id enviado exitosamente al servidor AssistIA\n");

    return true;
}

function plugin_glpiassistia_change_profile()
{
    // Función requerida por GLPI
}

function plugin_glpiassistia_postinit()
{
    // Función requerida por GLPI
}