<?php

if (!defined('GLPI_ROOT')) {
    define('GLPI_ROOT', dirname(dirname(dirname(__FILE__))));
}

include_once(__DIR__ . '/hook.php');

spl_autoload_register(function ($class) {
    if (strpos($class, 'GlpiPlugin\\AssistIA\\') === 0) {
        $class_file = str_replace('GlpiPlugin\\AssistIA\\', '', $class);
        $class_file = __DIR__ . '/src/' . $class_file . '.php';
        if (file_exists($class_file)) {
            require_once $class_file;
        }
    }
});

function plugin_init_glpiassistia()
{
    global $PLUGIN_HOOKS;

    $PLUGIN_HOOKS['csrf_compliant']['glpiassistia'] = true;
    $PLUGIN_HOOKS['change_profile']['glpiassistia'] = 'plugin_glpiassistia_change_profile';
    $PLUGIN_HOOKS['post_init']['glpiassistia'] = 'plugin_glpiassistia_postinit';

    $PLUGIN_HOOKS['item_add']['glpiassistia'] = [
        'Ticket' => 'plugin_glpiassistia_trigger_ia_on_ticket'
    ];
    
    $PLUGIN_HOOKS['post_item_form']['glpiassistia'] = [
        'Ticket' => 'plugin_glpiassistia_post_item_form'
    ];

    $PLUGIN_HOOKS['menu_toadd']['glpiassistia'] = [
        'config' => 'PluginGlpiassistiaConfig'
    ];

    $PLUGIN_HOOKS['config_page']['glpiassistia'] = 'front/config.php';

    $PLUGIN_HOOKS['add_css']['glpiassistia'] = 'glpiassistia.css';
    $PLUGIN_HOOKS['add_javascript']['glpiassistia'] = 'glpiassistia.js';
}

function plugin_version_glpiassistia()
{
    return [
        'name'           => 'GLPI AssistIA',
        'version'        => '1.0.0',
        'author'         => 'ANFAIA - Anxo López Rodríguez - Miguel Gonzalez (Aitire)',
        'license'        => 'GPL v3+',
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
        echo "Este plugin requiere GLPI >= 10.0.0";
        return false;
    }
    return true;
}

function plugin_glpiassistia_check_config($verbose = false)
{
    $config = \Config::getConfigurationValues('plugin:AssistIA');
    
    if (isset($config['server_url']) && !empty($config['server_url'])) {
        return true;
    }

    if ($verbose) {
        echo 'Plugin instalado pero no configurado. Por favor, configure la URL del servidor AssistIA.';
    }
    return false;
}

function plugin_glpiassistia_install()
{
    include_once(__DIR__ . '/install/install.php');
    return plugin_glpi_assistia_install();
}

function plugin_glpiassistia_uninstall()
{
    include_once(__DIR__ . '/install/install.php');
    return plugin_glpi_assistia_uninstall();
}