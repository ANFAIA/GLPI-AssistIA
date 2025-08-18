<?php
function plugin_glpiassistia_trigger_ia_on_ticket($ticket) {
    if ($ticket->getType() !== 'Ticket') {
        return true;
    }

    $ticket_id = $ticket->getID();
    $title = isset($ticket->fields['name']) ? $ticket->fields['name'] : '';
    $content = isset($ticket->fields['content']) ? $ticket->fields['content'] : '';
    $requester_id = isset($ticket->fields['users_id_recipient']) ? (int)$ticket->fields['users_id_recipient'] : null;
    $priority = isset($ticket->fields['priority']) ? (int)$ticket->fields['priority'] : null;
    $urgency = isset($ticket->fields['urgency']) ? (int)$ticket->fields['urgency'] : null;
    $impact = isset($ticket->fields['impact']) ? (int)$ticket->fields['impact'] : null;

    $payload = array(
        'ticket' => array(
            'id' => $ticket_id,
            'title' => $title,
            'content' => $content,
            'requester_id' => $requester_id,
            'priority' => $priority,
            'urgency' => $urgency,
            'impact' => $impact,
        ),
        'source' => 'glpi',
        'event' => 'ticket_created'
    );

    $config = Config::getConfigurationValues('plugin:AssistIA');
    $server_url = isset($config['server_url']) && $config['server_url'] !== ''
        ? $config['server_url']
        : 'http://localhost:8000/run-agent';

    $ch = curl_init($server_url);
    $json = json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json);
    curl_setopt($ch, CURLOPT_TIMEOUT, 3);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
    $response = curl_exec($ch);
    if ($response === false) {

    }
    curl_close($ch);

    return true;
}

function plugin_glpiassistia_change_profile() {
}

function plugin_glpiassistia_postinit() {
}

