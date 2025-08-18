<?php

function plugin_init_glpiassistia()
{
    global $PLUGIN_HOOKS, $LANG;

    $PLUGIN_HOOKS['csrf_compliant']['glpiassistia'] = true;
    $PLUGIN_HOOKS['change_profile']['glpiassistia'] = 'plugin_glpiassistia_change_profile';
    $PLUGIN_HOOKS['post_init']['glpiassistia'] = 'plugin_glpiassistia_postinit';

    $PLUGIN_HOOKS['item_add']['glpiassistia'] = [
        'Ticket' => 'plugin_glpiassistia_trigger_ia_on_ticket'
    ];

    $PLUGIN_HOOKS['menu_toadd']['glpiassistia'] = [
        'plugins' => 'GlpiPlugin\AssistIA\AssistIA'
    ];

    $PLUGIN_HOOKS['add_css']['glpiassistia'] = 'glpissistia.css';
    $PLUGIN_HOOKS['add_javascript']['glpiassistia'] = 'glpiassistia.js';
}

function plugin_version_glpiassistia()
{
    return [
        'name'           => 'GLPI AssistIA (DEMO)',
        'version'        => '0.1.0',
        'author'         => 'ANFAIA',
        'license'        => 'N/A',
        'homepage'       => 'https://github.com/ANFAIA/GLPI-AssistIA',
        'requirements'   => [
            'glpi' => [
                'min' => '10.0.0',
                'max' => '11.0.0'
            ]
        ]
    ];
}

function plugin_glpiassistia_check_prerequisites()
{
    if (version_compare(GLPI_VERSION, '10.0.0', 'lt')) {
        echo "This plugin requires GLPI >= 10.0.0";
        return false;
    }
    return true;
}

function plugin_glpiassistia_check_config($verbose = false)
{
    if (true) { // Your configuration check
        return true;
    }

    if ($verbose) {
        echo 'Installed / not configured';
    }
    return false;
}

function plugin_glpiassistia_install() {
    return true;
}

function plugin_glpiassistia_uninstall() {
    return true;
}

