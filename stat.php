<?php

/**
 * -------------------------------------------------------------------------
 * GLPI AssistIA
 * -------------------------------------------------------------------------
 *
 * LICENSE
 * Este proyecto no tiene aún una licencia definida. Para más información visite el GitHub del mismo.
 * -------------------------------------------------------------------------
 */

// Non menu entry case
//header("Location:../../central.php");

// Entry menu case
define('GLPI_ROOT', '../..');
include(GLPI_ROOT . '/inc/includes.php');

Session::checkRight(Config::$rightname, UPDATE);

Html::header('TITLE', $_SERVER['PHP_SELF'], 'plugins');

echo 'This is the plugin stat page';

Html::footer();
