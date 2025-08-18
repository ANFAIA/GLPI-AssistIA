<?php
include('../../../inc/includes.php');

Session::checkRight('config', UPDATE);

Plugin::load('glpi_assistia');

Html::header('AssistIA Configuration', $_SERVER['PHP_SELF'], 'config', 'plugins');
Html::footer();


