<?php

// Non menu entry case
//header("Location:../../central.php");

// Entry menu case
define('GLPI_ROOT', '../..');
include(GLPI_ROOT . '/inc/includes.php');

Session::checkRight(Config::$rightname, UPDATE);

Html::header('TITRE', $_SERVER['PHP_SELF'], 'plugins');

echo 'This is the plugin report page';

Html::footer();
