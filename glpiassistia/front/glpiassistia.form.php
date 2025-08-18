<?php

use GlpiPlugin\AssistIA\AssistIA;

include('../../../inc/includes.php');
Session::checkLoginUser();

if ($_SESSION['glpiactiveprofile']['interface'] == 'central') {
    Html::header('AssistIA', $_SERVER['PHP_SELF'], 'plugins', AssistIA::class, '');
} else {
    Html::helpHeader('AssistIA', $_SERVER['PHP_SELF']);
}

$assistia = new AssistIA();
$assistia->display($_GET);

Html::footer();


