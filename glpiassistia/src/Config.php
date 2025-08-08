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
        $input['configuration'] = 1 - $input['configuration'];

        return $input;
    }

    public function showFormExample()
    {
        global $CFG_GLPI;

        if (!Session::haveRight('config', UPDATE)) {
            return false;
        }

        $my_config = GlpiConfig::getConfigurationValues('plugin:AssistIA');

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


