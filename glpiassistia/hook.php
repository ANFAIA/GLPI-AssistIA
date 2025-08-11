<?php

/**
 * -------------------------------------------------------------------------
 * Plugin GLPI AssistIA
 * -------------------------------------------------------------------------
 *
 * Este archivo es parte de GLPI AssistIA.
 *
 * Este plugin se basa en el plugin "Example" para GLPI.
 * Modificaciones copyright (C) 2024 por ANFAIA.
 * -------------------------------------------------------------------------
 * @link      https://github.com/ANFAIA/glpi-assistia
 * -------------------------------------------------------------------------
 */

/**
 * @param Ticket
 * @return bool
 */
function plugin_glpiassistia_trigger_ia_on_ticket($ticket) {
    if ($ticket->getType() == 'Ticket') {
        $ticket_id = $ticket->getID();
        $title = isset($ticket->fields['name']) ? $ticket->fields['name'] : '';
        $content = isset($ticket->fields['content']) ? $ticket->fields['content'] : '';

        $ticket_data = array(
            'numero'    => $ticket_id,
            'titulo'    => $title,
            'contenido' => $content
        );

        $json_ticket = json_encode($ticket_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

        // Rutas absolutas basadas en la ubicación del plugin
        $repo_root = realpath(__DIR__ . DIRECTORY_SEPARATOR . '..');
        $crew_dir = $repo_root . DIRECTORY_SEPARATOR . 'CrewAi';
        $python_script_path = $crew_dir . DIRECTORY_SEPARATOR . 'main.py';
        $log_file = $crew_dir . DIRECTORY_SEPARATOR . 'python_execution.log';
        $python_executable = 'python3';

        $escaped_json = escapeshellarg($json_ticket);

        // Ejecutar el script en background, redirigiendo salida a log
        $command = 'cd ' . escapeshellarg($crew_dir)
                 . ' && ' . $python_executable . ' ' . escapeshellarg($python_script_path)
                 . ' ' . $escaped_json
                 . ' >> ' . escapeshellarg($log_file) . ' 2>&1 &';

        shell_exec($command);
    }

    return true;
}

function plugin_glpiassistia_change_profile() {
}

function plugin_glpiassistia_postinit() {
}

