<?php

use GlpiPlugin\AssistIA\AssistIA;

include('../../../inc/includes.php');
Session::checkRight(AssistIA::$rightname, READ);

if ($_SESSION['glpiactiveprofile']['interface'] == 'central') {
    Html::header('AssistIA', $_SERVER['PHP_SELF'], 'plugins', AssistIA::class, '');
} else {
    Html::helpHeader('AssistIA', $_SERVER['PHP_SELF']);
}

Search::show(AssistIA::class);

Html::footer();


