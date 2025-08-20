<?php

/**
 * -------------------------------------------------------------------------
 * Plugin GLPI AssistIA
 * -------------------------------------------------------------------------
 * Este archivo es parte de GLPI AssistIA.
 *
 * Plugin para integración con servidor de IA para procesamiento automático
 * de incidencias en GLPI.
 * -------------------------------------------------------------------------
 * @copyright Copyright (C) 2024 por ANFAIA.
 * @link      https://github.com/ANFAIA/glpi_assistia
 * -------------------------------------------------------------------------
 */

function plugin_glpi_assistia_install()
{

    
    $default_config = [
        'server_url' => '',
        'enabled' => 0,
        'timeout' => 10,
    ];

    \Config::setConfigurationValues('plugin:AssistIA', $default_config);

    // Crear directorio de logs si no existe
    $log_dir = GLPI_LOG_DIR;
    if (!is_dir($log_dir)) {
        mkdir($log_dir, 0755, true);
    }

    Toolbox::logInFile('glpi_assistia', "Plugin AssistIA instalado correctamente\n");

    return true;
}

function plugin_glpi_assistia_uninstall()
{
    $config = new \Config();
    $config->deleteByCriteria(['context' => 'plugin:AssistIA']);

    // Registrar en log la desinstalación
    Toolbox::logInFile('glpi_assistia', "Plugin AssistIA desinstalado correctamente\n");

    return true;
}

/**
 * Actualizar plugin de una versión a otra
 */
function plugin_glpi_assistia_update($current_version)
{
    // Por ahora no hay actualizaciones específicas
    return true;
}