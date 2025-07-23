<?php

namespace GlpiPlugin\GlpiAssistia;

use CommonDBTM;
use CommonGLPI;

class AssistIA extends CommonDBTM
{
    public static $rightname = 'plugin_glpi_assistia';

    public static function getMenuName()
    {
        return __('AssistIA', 'glpi_assistia');
    }

    public function getTabNameForItem(CommonGLPI $item, $withtemplate = 0)
    {
        if ($item->getType() == 'Config') {
            return __('GLPI AssistIA');
        }
        return '';
    }

    public static function displayTabContentForItem(CommonGLPI $item, $tabnum = 1, $withtemplate = 0)
    {
        if ($item->getType() == 'Config') {
            $config = new Config();
            $config->showForm();
        }
        return true;
    }
}