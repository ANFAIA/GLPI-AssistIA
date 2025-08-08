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

// Non menu entry case
//header("Location:../../central.php");

// Entry menu case
include('../../../inc/includes.php');

Session::checkRight('config', UPDATE);

// To be available when plugin in not activated
Plugin::load('glpi_assistia');

Html::header('AssistIA Configuration', $_SERVER['PHP_SELF'], 'config', 'plugins');
echo __('This is the AssistIA plugin config page', 'assistia');
Html::footer();


