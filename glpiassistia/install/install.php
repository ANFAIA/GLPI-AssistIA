<?php

/**
 * -------------------------------------------------------------------------
 * Plugin GLPI AssistIA
 * -------------------------------------------------------------------------
 * Este archivo es parte de GLPI AssistIA.
 *
 * Este plugin se basa en el plugin "Example" para GLPI.
 * Modificaciones copyright (C) 2024 por ANFAIA.
 * -------------------------------------------------------------------------
 * @copyright Copyright (C) 2024 by ANFAIA.
 * @link      https://github.com/ANFAIA/glpi_assistia
 * -------------------------------------------------------------------------
 */

function plugin_glpi_assistia_install()
{
    global $DB;

    $tables = [
        'glpi_plugin_assistia_assistias' => [
            'id' => 'int unsigned NOT NULL AUTO_INCREMENT',
            'name' => 'varchar(255) NOT NULL',
            'serial' => 'varchar(255) DEFAULT NULL',
            'entities_id' => 'int unsigned NOT NULL DEFAULT 0',
            'is_recursive' => 'tinyint(1) NOT NULL DEFAULT 0',
            'comment' => 'text',
            'date_mod' => 'timestamp NULL DEFAULT NULL',
            'date_creation' => 'timestamp NULL DEFAULT NULL',
            'PRIMARY KEY' => '(id)',
            'KEY' => 'entities_id (entities_id)',
            'KEY' => 'is_recursive (is_recursive)',
            'KEY' => 'date_mod (date_mod)',
            'KEY' => 'date_creation (date_creation)'
        ]
    ];

    foreach ($tables as $table => $fields) {
        if (!$DB->tableExists($table)) {
            $query = "CREATE TABLE `$table` (";
            $query_fields = [];
            foreach ($fields as $field => $definition) {
                if ($field === 'PRIMARY KEY' || $field === 'KEY') {
                    $query_fields[] = "$field $definition";
                } else {
                    $query_fields[] = "`$field` $definition";
                }
            }
            $query .= implode(', ', $query_fields);
            $query .= ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;";
            
            $DB->query($query);
        }
    }

    $config = new \GlpiPlugin\AssistIA\Config();
    $config->add([
        'configuration' => 1
    ]);

    return true;
}

function plugin_glpi_assistia_uninstall()
{
    global $DB;

    $tables = [
        'glpi_plugin_assistia_assistias'
    ];

    foreach ($tables as $table) {
        if ($DB->tableExists($table)) {
            $DB->query("DROP TABLE `$table`");
        }
    }

    $config = new \GlpiPlugin\AssistIA\Config();
    $config->deleteByCriteria(['configuration' => 1]);

    return true;
}



