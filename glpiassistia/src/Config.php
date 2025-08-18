<?php
namespace GlpiPlugin\AssistIA;

use CommonDBTM;
use CommonGLPI;
use Config as GlpiConfig;
use Dropdown;
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
                return __('AssistIA plugin');
            }
        }

        return '';
    }

    public static function configUpdate($input)
    {
        $current = GlpiConfig::getConfigurationValues('plugin:AssistIA');
        $new_values = [
            'configuration' => isset($input['configuration']) ? (int)$input['configuration'] : (int)($current['configuration'] ?? 0),
            'server_url'    => isset($input['server_url']) ? trim($input['server_url']) : ($current['server_url'] ?? ''),
        ];

        GlpiConfig::setConfigurationValues('plugin:AssistIA', $new_values);

        return array_merge($input, $new_values);
    }

    public function showFormExample()
    {
        global $CFG_GLPI;

        if (!Session::haveRight('config', UPDATE)) {
            return false;
        }

        $my_config = GlpiConfig::getConfigurationValues('plugin:AssistIA');
        $server_url_value = isset($my_config['server_url']) && $my_config['server_url'] !== ''
            ? $my_config['server_url']
            : 'http://localhost:8000/run-agent';

        echo "<form name='form' action=\"" . Toolbox::getItemTypeFormURL('Config') . "\" method='post'>";
        echo "<div class='center' id='tabsbody'>";
        echo "<table class='tab_cadre_fixe'>";
        echo "<tr><th colspan='4'>" . __('AssistIA setup') . '</th></tr>';
        echo '<td >' . __('My boolean choice :') . '</td>';
        echo "<td colspan='3'>";
        echo "<input type='hidden' name='config_class' value='" . __CLASS__ . "'>";
        echo "<input type='hidden' name='config_context' value='plugin:AssistIA'>";
        Dropdown::showYesNo('configuration', $my_config['configuration']);
        echo '</td></tr>';

        echo "<tr class='tab_bg_1'>";
        echo '<td>' . __('AssistIA server URL', 'assistia') . '</td>';
        echo "<td colspan='3'>";
        echo "<input type='text' name='server_url' size='80' value='" . Html::cleanInputText($server_url_value) . "'>";
        echo '</td></tr>';

        echo "<tr class='tab_bg_2'>";
        echo "<td colspan='4' class='center'>";
        echo "<input type='submit' name='update' class='submit' value=\"" . _sx('button', 'Save') . '">';
        echo '</td></tr>';

        echo '</table></div>';
        Html::closeForm();
    }

    public static function displayTabContentForItem(CommonGLPI $item, $tabnum = 1, $withtemplate = 0)
    {
        if ($item->getType() == 'Config') {
            $config = new self();
            $config->showFormExample();
        }
    }
}


