<?php

namespace GlpiPlugin\AssistIA;

use CommonDBTM;
use CommonGLPI;
use Config as GlpiConfig;
use Html;
use Session;
use Toolbox;

class Config extends CommonDBTM
{
    protected static $notable = true;

    public function getTabNameForItem(CommonGLPI $item, $withtemplate = 0)
    {
        if (!$withtemplate) {
            if ($item->getType() == 'Config') {
                return __('AssistIA Plugin', 'glpiassistia');
            }
        }
        return '';
    }

    public static function configUpdate($input)
    {
        $current = GlpiConfig::getConfigurationValues('plugin:AssistIA');
        
        $server_url = isset($input['server_url']) ? trim($input['server_url']) : '';
        
        if (!empty($server_url)) {
            if (!filter_var($server_url, FILTER_VALIDATE_URL)) {
                Session::addMessageAfterRedirect(
                    __('URL del servidor inválida', 'glpiassistia'), 
                    false, 
                    ERROR
                );
                return false;
            }
        }

        $new_values = [
            'server_url' => $server_url,
            'enabled' => isset($input['enabled']) ? (int)$input['enabled'] : 0,
            'timeout' => isset($input['timeout']) ? max(1, min(60, (int)$input['timeout'])) : 10,
        ];

        GlpiConfig::setConfigurationValues('plugin:AssistIA', $new_values);

        Session::addMessageAfterRedirect(
            __('Configuración guardada con éxito', 'glpiassistia'), 
            false, 
            INFO
        );

        return true;
    }

    public function showFormConfig()
    {
        if (!Session::haveRight('config', UPDATE)) {
            return false;
        }

        $config = GlpiConfig::getConfigurationValues('plugin:AssistIA');
        $server_url = $config['server_url'] ?? '';
        $enabled = $config['enabled'] ?? 0;
        $timeout = $config['timeout'] ?? 10;

        echo "<form name='form' action=\"" . Toolbox::getItemTypeFormURL('Config') . "\" method='post'>";
        echo "<div class='center' id='tabsbody'>";
        echo "<table class='tab_cadre_fixe'>";
        
        echo "<tr><th colspan='2'>" . __('Configuración GLPI AssistIA', 'glpiassistia') . '</th></tr>';
        
        echo "<tr class='tab_bg_1'>";
        echo "<td>" . __('Habilitar GLPI AssistIA', 'glpiassistia') . "</td>";
        echo "<td>";
        echo "<input type='hidden' name='config_class' value='" . __CLASS__ . "'>";
        echo "<input type='hidden' name='config_context' value='plugin:AssistIA'>";
        \Dropdown::showYesNo('enabled', $enabled);
        echo "</td></tr>";
        
        echo "<tr class='tab_bg_1'>";
        echo "<td>" . __('URL del servidor AssistIA (AssistIA Server)', 'glpiassistia') . "</td>";
        echo "<td>";
        echo "<input type='url' name='server_url' size='80' value='" . 
              Html::cleanInputText($server_url) . "' placeholder='http://localhost:8000/run-agent'>";
        echo "<br><small>" . __('Ejemplo: http://servidor.com:8000/run-agent | Si usas Docker utiliza host.docker.internal en vez de localhost o similar', 'glpiassistia') . "</small>";
        echo "</td></tr>";
        
        echo "<tr class='tab_bg_1'>";
        echo "<td>" . __('Timeout de conexión (segundos)', 'glpiassistia') . "</td>";
        echo "<td>";
        echo "<input type='number' name='timeout' min='1' max='60' value='$timeout'>";
        echo "<br><small>" . __('Tiempo máximo de espera para la conexión (1-60 segundos)', 'glpiassistia') . "</small>";
        echo "</td></tr>";

        echo "<tr class='tab_bg_2'>";
        echo "<td colspan='2' class='center'>";
        echo "<input type='submit' name='update' class='btn btn-primary' value=\"" . 
              _sx('button', 'Guardar') . '">';
        echo "</td></tr>";

        echo "</table></div>";
        Html::closeForm();

    }

    public static function displayTabContentForItem(CommonGLPI $item, $tabnum = 1, $withtemplate = 0)
    {
        if ($item->getType() == 'Config') {
            $config = new self();
            $config->showFormConfig();
        }
        return true;
    }
}