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

// ----------------------------------------------------------------------
// Original Author of file:
// Purpose of file:
// ----------------------------------------------------------------------

use GlpiPlugin\AssistIA\AssistIA;

include('../../../inc/includes.php');
Session::checkRight(AssistIA::$rightname, READ);

if ($_SESSION['glpiactiveprofile']['interface'] == 'central') {
    Html::header('AssistIA', $_SERVER['PHP_SELF'], 'plugins', AssistIA::class, '');
} else {
    Html::helpHeader('AssistIA', $_SERVER['PHP_SELF']);
}


//checkTypeRight(AssistIA::class,"r");

Search::show(AssistIA::class);

Html::footer();


