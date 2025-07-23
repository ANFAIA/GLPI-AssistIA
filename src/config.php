<?php

namespace GlpiPlugin\GlpiAssistia;

use CommonDBTM;
use CommonGLPI;
use Config as GlpiConfig;
use Dropdown;
use Html;
use Session;
use Toolbox;

class Config extends CommonDBTM
{
    public function getTabNameForItem(CommonGLPI $item, $withtemplate = 0)
    {
        if ($item->getType() == 'Config') {
            return __('AssistIA', 'glpi_assistia');
        }
        return '';
    }

    public function showForm()
    {
        if (!Session::haveRight('config', UPDATE)) {
            return false;
        }

        $my_config = GlpiConfig::getConfigurationValues('plugin:GlpiAssistia');

        echo "<form name='form' action=\"" . Toolbox::getItemTypeFormURL('Config') . "\" method='post'>";
        Html::openForm();

        echo "<div class='center' id='tabsbody'>";
        echo "<table class='tab_cadre_fixe'>";
        echo "<tr><th colspan='4'>" . __('Configuración de AssistIA', 'glpi_assistia') . "</th></tr>";
        
        echo "<tr class='tab_bg_1'><td>" . __('Activar funcionalidad X:', 'glpi_assistia') . "</td>";
        echo "<td colspan='3'>";
        $config_value = $my_config['configuration'] ?? 0;
        Dropdown::showYesNo('configuration', $config_value);
        echo "</td></tr>";

        echo "<tr class='tab_bg_2'>";
        echo "<td colspan='4' class='center'>";
        echo "<input type='hidden' name='_glpi_csrf_token' value='" . Session::getNewCSRFToken() . "'>";
        echo "<input type='hidden' name='config_class' value='" . __CLASS__ . "'>";
        echo "<input type='hidden' name='config_context' value='plugin:GlpiAssistia'>";
        echo "<input type='submit' name='update' class='submit' value=\"" . _sx('button', 'Save') . "\">";
        echo "</td></tr>";

        echo "</table></div>";
        Html::closeForm();
        echo "</form>";
    }

    public static function displayTabContentForItem(CommonGLPI $item, $tabnum = 1, $withtemplate = 0)
    {
        if ($item->getType() == 'Config') {
            $config = new self();
            $config->showForm();
        }
    }
}