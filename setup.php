<?php


use Glpi\Plugin\Hooks;
use GlpiPlugin\GlpiAssistia\Computer;
use GlpiPlugin\GlpiAssistia\Config;
use GlpiPlugin\GlpiAssistia\Dropdown;
use GlpiPlugin\GlpiAssistia\DeviceCamera;
use GlpiPlugin\GlpiAssistia\AssistIA; // Cambiado de Example a AssistIA
use GlpiPlugin\GlpiAssistia\Filters\ComputerModelFilter;
use GlpiPlugin\GlpiAssistia\ItemForm;
use GlpiPlugin\GlpiAssistia\RuleTestCollection;
use GlpiPlugin\GlpiAssistia\Showtabitem;

define('PLUGIN_GLPIASSISTIA_VERSION', '0.1.0');

// Minimal GLPI version, inclusive
define('PLUGIN_GLPIASSISTIA_MIN_GLPI', '10.0.0');
// Maximum GLPI version, exclusive
define('PLUGIN_GLPIASSISTIA_MAX_GLPI', '10.0.99');

/**
 * Init hooks of the plugin.
 * REQUIRED
 *
 * @return void
 */
function plugin_init_glpi_assistia() 
{
    global $PLUGIN_HOOKS, $CFG_GLPI;

    Plugin::registerClass(Config::class, ['addtabon' => 'Config']);
    Plugin::registerClass(Dropdown::class);

    $types = ['Central', 'Computer', 'ComputerDisk', 'Notification', 'Phone',
        'Preference', 'Profile', 'Supplier'];
    Plugin::registerClass(
        AssistIA::class,
        ['notificationtemplates_types' => true,
            'addtabon'                 => $types,
            'link_types'               => true],
    );

    Plugin::registerClass(
        RuleTestCollection::class,
        ['rulecollections_types' => true],
    );

    Plugin::registerClass(
        DeviceCamera::class,
        ['device_types' => true],
    );

    if (version_compare(GLPI_VERSION, '9.1', 'ge')) {
        if (class_exists(AssistIA::class)) { 
            Link::registerTag(AssistIA::$tags);
        }
    }
    
    Plugin::registerClass(\GlpiPlugin\GlpiAssistia\Profile::class, ['addtabon' => ['Profile']]);
    if (AssistIA::canView()) { 
        $PLUGIN_HOOKS['menu_toadd']['glpi_assistia'] = ['plugins' => AssistIA::class,
                                                     'tools' => AssistIA::class];

        $PLUGIN_HOOKS[Hooks::HELPDESK_MENU_ENTRY]['glpi_assistia']      = true;
        $PLUGIN_HOOKS[Hooks::HELPDESK_MENU_ENTRY_ICON]['glpi_assistia'] = 'fas fa-puzzle-piece';
    }

    if (Session::haveRight('config', UPDATE)) {
        $PLUGIN_HOOKS['config_page']['glpi_assistia'] = 'front/config.php';
    }
    
    $PLUGIN_HOOKS['change_profile']['glpi_assistia'] = 'plugin_change_profile_glpi_assistia';
    $PLUGIN_HOOKS[Hooks::PRE_ITEM_UPDATE]['glpi_assistia'] = [Computer::class => 'plugin_pre_item_update_glpi_assistia'];
    $PLUGIN_HOOKS[hooks::ITEM_UPDATE]['glpi_assistia']     = [Computer::class => 'plugin_item_update_glpi_assistia'];
    $PLUGIN_HOOKS[Hooks::ITEM_EMPTY]['glpi_assistia'] = [Computer::class => 'plugin_item_empty_glpi_assistia'];
    $PLUGIN_HOOKS[Hooks::ITEM_CAN]['glpi_assistia']     = [Computer::class => [AssistIA::class, 'item_can']];
    $PLUGIN_HOOKS['add_default_where']['glpi_assistia'] = [Computer::class => [AssistIA::class, 'add_default_where']];

    $PLUGIN_HOOKS[Hooks::PRE_ITEM_ADD]['glpi_assistia'] = [Computer::class => [AssistIA::class,
        'pre_item_add_computer']];
    $PLUGIN_HOOKS[Hooks::POST_PREPAREADD]['glpi_assistia'] = [Computer::class => [AssistIA::class,
        'post_prepareadd_computer']];
    $PLUGIN_HOOKS[Hooks::ITEM_ADD]['glpi_assistia'] = [Computer::class => [AssistIA::class,
        'item_add_computer']];

    $PLUGIN_HOOKS[Hooks::PRE_ITEM_DELETE]['glpi_assistia'] = [Computer::class => 'plugin_pre_item_delete_glpi_assistia'];
    $PLUGIN_HOOKS[Hooks::ITEM_DELETE]['glpi_assistia']     = [Computer::class => 'plugin_item_delete_glpi_assistia'];

    $PLUGIN_HOOKS[Hooks::PRE_ITEM_PURGE]['glpi_assistia'] = [Computer::class => 'plugin_pre_item_purge_glpi_assistia',
        'Phone'                                                        => 'plugin_pre_item_purge_glpi_assistia'];
    $PLUGIN_HOOKS[Hooks::ITEM_PURGE]['glpi_assistia'] = [Computer::class => 'plugin_item_purge_glpi_assistia',
        'Phone'                                                    => 'plugin_item_purge_glpi_assistia'];

    $PLUGIN_HOOKS[Hooks::PRE_ITEM_RESTORE]['glpi_assistia'] = [Computer::class => 'plugin_pre_item_restore_glpi_assistia',
        'Phone'                                                          => 'plugin_pre_item_restore_glpi_assistia2'];
    $PLUGIN_HOOKS[Hooks::ITEM_RESTORE]['glpi_assistia'] = [Computer::class => 'plugin_item_restore_glpi_assistia'];

    $PLUGIN_HOOKS[Hooks::ITEM_GET_EVENTS]['glpi_assistia']
                                  = ['NotificationTargetTicket' => 'plugin_glpi_assistia_get_events'];

    $PLUGIN_HOOKS[Hooks::ITEM_GET_DATA]['glpi_assistia']
                                  = ['NotificationTargetTicket' => 'plugin_glpi_assistia_get_datas'];

    $PLUGIN_HOOKS[Hooks::ITEM_TRANSFER]['glpi_assistia'] = 'plugin_item_transfer_glpi_assistia';

    $CFG_GLPI['planning_types'][] = AssistIA::class;

    $PLUGIN_HOOKS['use_massive_action']['glpi_assistia'] = 1;
    $PLUGIN_HOOKS['assign_to_ticket']['glpi_assistia'] = 1;

    $PLUGIN_HOOKS[Hooks::ADD_JAVASCRIPT]['glpi_assistia'] = 'glpi_assistia.js';
    $PLUGIN_HOOKS[Hooks::ADD_CSS]['glpi_assistia']        = 'glpi_assistia.css';
    
    $PLUGIN_HOOKS[Hooks::POST_INIT]['glpi_assistia'] = 'plugin_glpi_assistia_postinit';

    $PLUGIN_HOOKS['status']['glpi_assistia'] = 'plugin_glpi_assistia_Status';
    $PLUGIN_HOOKS[Hooks::CSRF_COMPLIANT]['glpi_assistia'] = true;
$PLUGIN_HOOKS[Hooks::DISPLAY_CENTRAL]['glpi_assistia']  = 'plugin_glpi_assistia_display_central';
    $PLUGIN_HOOKS[Hooks::DISPLAY_LOGIN]['glpi_assistia']    = 'plugin_glpi_assistia_display_login';
    $PLUGIN_HOOKS[Hooks::INFOCOM]['glpi_assistia']          = 'plugin_glpi_assistia_infocom_hook';

    $PLUGIN_HOOKS[Hooks::PRE_SHOW_TAB]['glpi_assistia']    = [Showtabitem::class, 'pre_show_tab'];
    $PLUGIN_HOOKS[Hooks::POST_SHOW_TAB]['glpi_assistia']   = [Showtabitem::class, 'post_show_tab'];
    $PLUGIN_HOOKS[Hooks::PRE_SHOW_ITEM]['glpi_assistia']   = [Showtabitem::class, 'pre_show_item'];
    $PLUGIN_HOOKS[Hooks::POST_SHOW_ITEM]['glpi_assistia']  = [Showtabitem::class, 'post_show_item'];

    $PLUGIN_HOOKS[Hooks::PRE_ITEM_FORM]['glpi_assistia']   = [ItemForm::class, 'preItemForm'];
    $PLUGIN_HOOKS[Hooks::POST_ITEM_FORM]['glpi_assistia']  = [ItemForm::class, 'postItemForm'];

    $PLUGIN_HOOKS[Hooks::TIMELINE_ACTIONS]['glpi_assistia'] = [ItemForm::class, 'timelineActions'];
    $PLUGIN_HOOKS[Hooks::FILTER_ACTORS]['glpi_assistia']    = 'plugin_glpi_assistia_filter_actors';

    $PLUGIN_HOOKS['dashboard_types']['glpi_assistia']      = [AssistIA::class, 'dashboardTypes'];
    $PLUGIN_HOOKS['dashboard_cards']['glpi_assistia']      = [AssistIA::class, 'dashboardCards'];

    $PLUGIN_HOOKS[Hooks::DASHBOARD_FILTERS]['glpi_assistia'] = [ComputerModelFilter::class];

}


/**
 * Get the name and the version of the plugin
 * REQUIRED
 *
 * @return array
 */
function plugin_version_glpi_assistia()
{
    return [
        'name'         => 'GLPI AssistIA',
        'version'      => PLUGIN_GLPIASSISTIA_VERSION,
        'author'       => 'ANFAIA',
        'license'      => 'GPLv2+',
        'homepage'     => 'https://github.com/ANFAIA/GLPI-AssistIA',
        'requirements' => [
            'glpi' => [
                'min' => PLUGIN_GLPIASSISTIA_MIN_GLPI,
                'max' => PLUGIN_GLPIASSISTIA_MAX_GLPI,
            ],
        ],
    ];
}


/**
 * Check pre-requisites before install
 * OPTIONNAL, but recommanded
 *
 * @return boolean
 */
function plugin_glpi_assistia_check_prerequisites() // Cambiado
{
    // Lógica de pre-requisitos
    return true;
}

/**
 * Check configuration process
 *
 * @param boolean $verbose Whether to display message on failure. Defaults to false
 *
 * @return boolean
 */
function plugin_glpi_assistia_check_config($verbose = false)
{
    if (true) { // Lógica de comprobación
        return true;
    }

    if ($verbose) {
        echo __('Installed / not configured', 'glpi_assistia');
    }

    return false;
}