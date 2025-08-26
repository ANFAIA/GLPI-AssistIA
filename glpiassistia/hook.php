<?php

function plugin_glpiassistia_trigger_ia_on_ticket($ticket)
{
    Toolbox::logInFile('glpi_assistia', "=== HOOK TRIGGERED ===\n");
    
    if (!$ticket instanceof Ticket) {
        Toolbox::logInFile('glpi_assistia', "Error: Objeto no es un Ticket\n");
        return true;
    }

    $ticket_id = $ticket->getID();
    $title = isset($ticket->fields['name']) ? $ticket->fields['name'] : '';
    $content = isset($ticket->fields['content']) ? $ticket->fields['content'] : '';

    Toolbox::logInFile('glpi_assistia', "Ticket ID: $ticket_id, Title: $title\n");

    $config = Config::getConfigurationValues('plugin:AssistIA');
    $enabled = isset($config['enabled']) ? (int)$config['enabled'] : 0;
    
    if (!$enabled) {
        Toolbox::logInFile('glpi_assistia', "Plugin deshabilitado, no se procesa ticket $ticket_id\n");
        return true;
    }

    $payload = [
        'id' => $ticket_id,
        'title' => $title,
        'description' => $content
    ];

    $server_url = isset($config['server_url']) && !empty($config['server_url'])
        ? rtrim($config['server_url'], '/')
        : null;

    if (!$server_url) {
        Toolbox::logInFile('glpi_assistia', 
            "Error: URL del servidor AssistIA no configurada para el ticket ID: $ticket_id\n");
        return true;
    }

    Toolbox::logInFile('glpi_assistia', "Enviando a: $server_url\n");
    Toolbox::logInFile('glpi_assistia', "Payload: " . json_encode($payload) . "\n");

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

    Toolbox::logInFile('glpi_assistia', "HTTP Code: $http_code, Response: $response\n");

    if ($response === false || !empty($curl_error)) {
        $error_msg = "Error de conexión con el servidor AssistIA para el ticket ID: $ticket_id - " . 
                     ($curl_error ?: 'Error desconocido');
        Toolbox::logInFile('glpi_assistia', $error_msg . "\n");
        
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

    // Mensaje de éxito al usuario
    if (isset($_SESSION['glpiactiveprofile'])) {
        Session::addMessageAfterRedirect(
            "Ticket enviado a AssistIA Server para procesamiento con IA.",
            false,
            INFO
        );
    }

    return true;
}

function plugin_glpiassistia_post_item_form($params)
{
    if ($params['item']->getType() == 'Ticket') {
        Toolbox::logInFile('glpi_assistia', "POST ITEM FORM hook triggered\n");
    }
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