<?php

namespace GlpiPlugin\AssistIA;

use CommonDBTM;
use CommonGLPI;
use Computer;
use Html;
use Log;
use MassiveAction;
use Session;

class AssistIA extends CommonDBTM
{
    public static $tags      = '[ASSISTIA_ID]';
    public static $rightname = 'plugin_assistia';

    public static function getTypeName($nb = 0)
    {
        return 'AssistIA Type';
    }

    public static function getMenuName()
    {
        return __('AssistIA plugin');
    }

    public static function getAdditionalMenuLinks()
    {
        global $CFG_GLPI;
        $links = [];

        $links['config']                                                                                                                         = '/plugins/glpiassistia/index.php';
        $links["<img  src='" . $CFG_GLPI['root_doc'] . "/pics/menu_showall.png' title='" . __s('Show all') . "' alt='" . __s('Show all') . "'>"] = '/plugins/glpiassistia/index.php';
        $links[__s('Test link', 'assistia')]                                                                                                      = '/plugins/glpiassistia/index.php';

        return $links;
    }

    public function defineTabs($options = [])
    {
        $ong = [];
        $this->addDefaultFormTab($ong);
        $this->addStandardTab('Link', $ong, $options);

        return $ong;
    }

    public function showForm($ID, array $options = [])
    {
        global $CFG_GLPI;

        $this->initForm($ID, $options);
        $this->showFormHeader($options);

        echo "<tr class='tab_bg_1'>";

        echo '<td>' . __('ID') . '</td>';
        echo '<td>';
        echo $ID;
        echo '</td>';

        $this->showFormButtons($options);

        return true;
    }

    public function rawSearchOptions()
    {
        $tab = [];

        $tab[] = [
            'id'   => 'common',
            'name' => __('Header Needed'),
        ];

        $tab[] = [
            'id'    => '1',
            'table' => 'glpi_plugin_assistia_assistias',
            'field' => 'name',
            'name'  => __('Name'),
        ];

        $tab[] = [
            'id'    => '2',
            'table' => 'glpi_plugin_assistia_dropdowns',
            'field' => 'name',
            'name'  => __('Dropdown'),
        ];

        $tab[] = [
            'id'         => '3',
            'table'      => 'glpi_plugin_assistia_assistias',
            'field'      => 'serial',
            'name'       => __('Serial number'),
            'usehaving'  => true,
            'searchtype' => 'equals',
        ];

        $tab[] = [
            'id'         => '30',
            'table'      => 'glpi_plugin_assistia_assistias',
            'field'      => 'id',
            'name'       => __('ID'),
            'usehaving'  => true,
            'searchtype' => 'equals',
        ];

        return $tab;
    }

    /**
     * Give localized information about 1 task
     *
     * @param $name of the task
     *
     * @return array of strings
     */
    public static function cronInfo($name)
    {
        switch ($name) {
            case 'Sample':
                return ['description' => __('Cron description for assistia', 'assistia'),
                    'parameter'       => __('Cron parameter for assistia', 'assistia')];
        }

        return [];
    }

    /**
     * Execute 1 task manage by the plugin
     *
     * @param $task Object of CronTask class for log / stat
     *
     * @return interger
     *    >0 : done
     *    <0 : to be run again (not finished)
     *     0 : nothing to do
     */
    public static function cronSample($task)
    {
        $task->log('AssistIA log message from class');
        $r = mt_rand(0, $task->fields['param']);
        usleep(1000000 + $r * 1000);
        $task->setVolume($r);

        return 1;
    }

    public static function pre_item_add_computer(Computer $item)
    {
        if (isset($item->input['name']) && empty($item->input['name'])) {
            Session::addMessageAfterRedirect('Pre Add Computer Hook KO (name empty)', true);

            return $item->input = false;
        } else {
            Session::addMessageAfterRedirect('Pre Add Computer Hook OK', true);
        }
    }

    public static function post_prepareadd_computer(Computer $item)
    {
        Session::addMessageAfterRedirect('Post prepareAdd Computer Hook', true);
    }

    public static function item_add_computer(Computer $item)
    {
        Session::addMessageAfterRedirect('Add Computer Hook, ID=' . $item->getID(), true);

        return true;
    }

    public function getTabNameForItem(CommonGLPI $item, $withtemplate = 0)
    {
        if (!$withtemplate) {
            switch ($item->getType()) {
                case 'Profile':
                    if ($item->getField('central')) {
                        return __('AssistIA', 'assistia');
                    }
                    break;

                case 'Phone':
                    if ($_SESSION['glpishow_count_on_tabs']) {
                        return self::createTabEntry(
                            __('AssistIA', 'assistia'),
                            countElementsInTable($this->getTable()),
                        );
                    }

                    return __('AssistIA', 'assistia');

                case 'ComputerDisk':
                case 'Supplier':
                    return [1 => __('Test Plugin', 'assistia'),
                        2     => __('Test Plugin 2', 'assistia')];

                case 'Computer':
                case 'Central':
                case 'Preference':
                case 'Notification':
                    return [1 => __('Test Plugin', 'assistia')];
            }
        }

        return '';
    }

    public static function displayTabContentForItem(CommonGLPI $item, $tabnum = 1, $withtemplate = 0)
    {
        return true;
    }

    public static function getSpecificValueToDisplay($field, $values, array $options = [])
    {
        if (!is_array($values)) {
            $values = [$field => $values];
        }
        switch ($field) {
            case 'serial':
                return 'S/N: ' . $values[$field];
        }

        return '';
    }

    public static function populatePlanning($parm)
    {

        $output                = [];
        $key                   = $parm['begin'] . '$$$' . 'plugin_assistia1';
        $output[$key]['begin'] = date('Y-m-d 17:00:00');
        $output[$key]['end']   = date('Y-m-d 18:00:00');
        $output[$key]['name']  = __('test planning assistia 1', 'assistia');
        $output[$key]['itemtype'] = AssistIA::class;
        $output[$key][getForeignKeyFieldForItemType(AssistIA::class)] = 1;

        return $output;
    }

    /**
     * Display a Planning Item
     *
     * @param $val Array of the item to display
     * @param $who ID of the user (0 if all)
     * @param $type position of the item in the time block (in, through, begin or end)
     * @param $complete complete display (more details)
     *
     * @return Nothing (display function)
     **/
    public static function displayPlanningItem(array $val, $who, $type = '', $complete = 0)
    {

        switch ($type) {
            case 'in':
                printf(
                    __('From %1$s to %2$s :'),
                    date('H:i', strtotime($val['begin'])),
                    date('H:i', strtotime($val['end'])),
                );
                break;

            case 'through':
                echo Html::resume_text($val['name'], 80);
                break;

            case 'begin':
                printf(__('Start at %s:'), date('H:i', strtotime($val['begin'])));
                break;

            case 'end':
                printf(__('End at %s:'), date('H:i', strtotime($val['end'])));
                break;
        }
        echo '<br>';
        echo Html::resume_text($val['name'], 80);
    }

    /**
     * Get an history entry message
     *
     * @param $data Array from glpi_logs table
     *
     * @since GLPI version 0.84
     *
     * @return string
    **/
    public static function getHistoryEntry($data)
    {
        switch ($data['linked_action'] - Log::HISTORY_PLUGIN) {
            case 0:
                return __('History from plugin assistia', 'assistia');
        }

        return '';
    }

    //////////////////////////////
    ////// SPECIFIC MODIF MASSIVE FUNCTIONS ///////
    public function getSpecificMassiveActions($checkitem = null)
    {
        $actions = parent::getSpecificMassiveActions($checkitem);

        $actions['Document_Item' . MassiveAction::CLASS_ACTION_SEPARATOR . 'add']  = _x('button', 'Add a document');         // GLPI core one
        $actions[__CLASS__ . MassiveAction::CLASS_ACTION_SEPARATOR . 'do_nothing'] = __('Do Nothing - just for fun', 'assistia');  // Specific one

        return $actions;
    }

    public static function showMassiveActionsSubForm(MassiveAction $ma)
    {
        switch ($ma->getAction()) {
            case 'DoIt':
                echo "&nbsp;<input type='hidden' name='toto' value='1'>" .
                     Html::submit(_x('button', 'Post'), ['name' => 'massiveaction']) .
                     ' ' . __('Write in item history', 'assistia');

                return true;
            case 'do_nothing':
                echo '&nbsp;' . Html::submit(_x('button', 'Post'), ['name' => 'massiveaction']) .
                     ' ' . __('but do nothing :)', 'assistia');

                return true;
        }

        return parent::showMassiveActionsSubForm($ma);
    }

    /**
     * @since version 0.85
     *
     * @see CommonDBTM::processMassiveActionsForOneItemtype()
    **/
    public static function processMassiveActionsForOneItemtype(
        MassiveAction $ma,
        CommonDBTM $item,
        array $ids
    ) {
        global $DB;

        switch ($ma->getAction()) {
            case 'DoIt':
                if ($item->getType() == 'Computer') {
                    Session::addMessageAfterRedirect(__('Right it is the type I want...', 'assistia'));
                    Session::addMessageAfterRedirect(__('Write in item history', 'assistia'));
                    $changes = [0, 'old value', 'new value'];
                    foreach ($ids as $id) {
                        if ($item->getFromDB($id)) {
                            Session::addMessageAfterRedirect('- ' . $item->getField('name'));
                            Log::history(
                                $id,
                                'Computer',
                                $changes,
                                AssistIA::class,
                                Log::HISTORY_PLUGIN,
                            );
                            $ma->itemDone($item->getType(), $id, MassiveAction::ACTION_OK);
                        } else {
                            // Example of ko count
                            $ma->itemDone($item->getType(), $id, MassiveAction::ACTION_KO);
                        }
                    }
                } else {
                    // When nothing is possible ...
                    $ma->itemDone($item->getType(), $ids, MassiveAction::ACTION_KO);
                }

                return;

            case 'do_nothing':
                if ($item->getType() == AssistIA::class) {
                    Session::addMessageAfterRedirect(__('Right it is the type I want...', 'assistia'));
                    Session::addMessageAfterRedirect(__(
                        'But... I say I will do nothing for:',
                        'assistia',
                    ));
                    foreach ($ids as $id) {
                        if ($item->getFromDB($id)) {
                            Session::addMessageAfterRedirect('- ' . $item->getField('name'));
                            $ma->itemDone($item->getType(), $id, MassiveAction::ACTION_OK);
                        } else {
                            // Example for noright / Maybe do it with can function is better
                            $ma->itemDone($item->getType(), $id, MassiveAction::ACTION_KO);
                        }
                    }
                } else {
                    $ma->itemDone($item->getType(), $ids, MassiveAction::ACTION_KO);
                }

                return;
        }
        parent::processMassiveActionsForOneItemtype($ma, $item, $ids);
    }

    public static function generateLinkContents($link, CommonDBTM $item)
    {
        if (strstr($link, '[ASSISTIA_ID]')) {
            $link = str_replace('[ASSISTIA_ID]', $item->getID(), $link);

            return [$link];
        }

        return parent::generateLinkContents($link, $item);
    }

    public static function dashboardTypes()
    {
        return [
            'assistia' => [
                'label'    => __('Plugin AssistIA', 'assistia'),
                'function' => AssistIA::class . '::cardWidget',
                'image'    => 'https://via.placeholder.com/100x86?text=assistia',
            ],
            'assistia_static' => [
                'label'    => __('Plugin AssistIA (static)', 'assistia'),
                'function' => AssistIA::class . '::cardWidgetWithoutProvider',
                'image'    => 'https://via.placeholder.com/100x86?text=assistia+static',
            ],
        ];
    }

    public static function dashboardCards($cards = [])
    {
        if (is_null($cards)) {
            $cards = [];
        }
        $new_cards = [
            'plugin_assistia_card' => [
                'widgettype' => ['assistia'],
                'label'      => __('Plugin AssistIA card'),
                'provider'   => AssistIA::class . '::cardDataProvider',
            ],
            'plugin_assistia_card_without_provider' => [
                'widgettype' => ['assistia_static'],
                'label'      => __('Plugin AssistIA card without provider'),
            ],
            'plugin_assistia_card_with_core_widget' => [
                'widgettype' => ['bigNumber'],
                'label'      => __('Plugin AssistIA card with core provider'),
                'provider'   => AssistIA::class . '::cardBigNumberProvider',
            ],
        ];

        return array_merge($cards, $new_cards);
    }

    public static function cardWidget(array $params = [])
    {
        $default = [
            'data'  => [],
            'title' => '',

            'color' => '',
        ];
        $p = array_merge($default, $params);

        $html = "<div class='card' style='background-color: {$p['color']};'>";
        $html .= "<h2>{$p['title']}</h2>";
        $html .= '<ul>';
        foreach ($p['data'] as $line) {
            $html .= "<li>$line</li>";
        }
        $html .= '</ul>';
        $html .= '</div>';

        return $html;
    }

    public static function cardDataProvider(array $params = [])
    {
        $default_params = [
            'label' => null,
            'icon'  => 'fas fa-smile-wink',
        ];
        $params = array_merge($default_params, $params);

        return [
            'title' => $params['label'],
            'icon'  => $params['icon'],
            'data'  => [
                'test1',
                'test2',
                'test3',
            ],
        ];
    }

    public static function cardWidgetWithoutProvider(array $params = [])
    {
        $default = [

            'color' => '',
        ];
        $p = array_merge($default, $params);

        $html = "<div class='card' style='background-color: {$p['color']};'>
                  static html (+optional javascript) as card is not matched with a data provider

                  <img src='https://www.linux.org/images/logo.png'>
               </div>";

        return $html;
    }

    public static function cardBigNumberProvider(array $params = [])
    {
        $default_params = [
            'label' => null,
            'icon'  => null,
        ];
        $params = array_merge($default_params, $params);

        return [
            'number' => rand(),
            'url'    => 'https://www.linux.org/',
            'label'  => 'plugin assistia - some text',
            'icon'   => 'fab fa-linux', // font awesome icon
        ];
    }
} 


