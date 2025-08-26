<?php

include('../../../inc/includes.php');

Session::checkLoginUser();

Plugin::load('glpiassistia');

if (isset($_POST['update']) && isset($_POST['config_class'])) {
    if ($_POST['config_class'] === 'PluginGlpiassistiaConfig') {
        PluginGlpiassistiaConfig::configUpdate($_POST);
        Html::back();
    }
}

Html::header('Configuración GLPI AssistIA', $_SERVER['PHP_SELF'], 'config', 'plugins');

echo "<div class='center'>";
echo "<h2>" . __('Plugin AssistIA - Configuración', 'glpiassistia') . "</h2>";

echo "<div class='card mb-3'>";
echo "<div class='card-body'>";
echo "<h5 class='card-title'>" . __('Información del Plugin', 'glpiassistia') . "</h5>";
echo "<p class='card-text'>";
echo __('Este plugin permite enviar automáticamente las incidencias creadas en GLPI a un servidor externo (GlpiassistIA Server) para procesamiento con IA.', 'glpiassistia');
echo "</p>";
echo "<p class='card-text'>";
echo "<strong>" . __('Versión:', 'glpiassistia') . "</strong> 1.0.0<br>";
echo "<strong>" . __('Autor:', 'glpiassistia') . "</strong> ANFAIA - Anxo López Rodríguez - Miguel Gonzalez";
echo "</p>";
echo "</div>";
echo "</div>";

PluginGlpiassistiaConfig::showForm();

echo "</div>";

Html::footer();