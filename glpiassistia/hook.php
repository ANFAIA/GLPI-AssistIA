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
        $title = $ticket->fields['name'];
        $content = $ticket->fields['content'];

        $full_content = "=== TICKET #{$ticket_id} - " . strtoupper($title) . " ===" . PHP_EOL . PHP_EOL;
        $full_content .= "TÍTULO: " . $title . PHP_EOL . PHP_EOL;
        $full_content .= "DESCRIPCIÓN INICIAL:" . PHP_EOL . $content;
        
        $ia_project_dir = '/var/www/html/glpi/files/_plugins/glpiassistia/glpiassistia-main/'; //Ruta de main.py
        $python_script_path = $ia_project_dir . 'CrewAi/main_demo.py';
        $incident_file_path = $ia_project_dir . 'CrewAi/incidencia.txt';
        $python_executable = 'python3';
        file_put_contents($incident_file_path, $full_content);
        $log_file = $ia_project_dir . 'python_execution.log';
        $command = "cd " . escapeshellarg($ia_project_dir . 'CrewAi/') . " && " . $python_executable . ' ' . escapeshellarg($python_script_path) . ' >> ' . escapeshellarg($log_file) . ' 2>&1 &';
        
        shell_exec($command);
    }
    
    return true;
}


function plugin_glpiassistia_change_profile() {
}

function plugin_glpiassistia_postinit() {
}

