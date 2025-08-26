<?php

class PluginGlpiassistiaConfig extends CommonGLPI
{
    public static function getMenuName()
    {
        return __('AssistIA Configuration', 'glpiassistia');
    }

    public static function getMenuContent()
    {
        $menu = [];
        $menu['title'] = self::getMenuName();
        $menu['page'] = '/plugins/glpiassistia/front/config.php';
        $menu['icon'] = 'fas fa-robot';
        
        return $menu;
    }

    public static function configUpdate($input)
    {
        $server_url = isset($input['server_url']) ? trim($input['server_url']) : '';
        
        if (!empty($server_url)) {
            if (!filter_var($server_url, FILTER_VALIDATE_URL)) {
                Session::addMessageAfterRedirect(
                    __('URL del servidor inválida', 'glpiassistia'), 
                    false, 
                    ERROR
                );
                return false;
            }
        }

        $new_values = [
            'server_url' => $server_url,
            'enabled' => isset($input['enabled']) ? (int)$input['enabled'] : 0,
            'timeout' => isset($input['timeout']) ? max(1, min(60, (int)$input['timeout'])) : 10,
        ];

        Config::setConfigurationValues('plugin:AssistIA', $new_values);

        Session::addMessageAfterRedirect(
            __('Configuración guardada exitosamente', 'glpiassistia'), 
            false, 
            INFO
        );

        return true;
    }

    public static function showForm()
    {


        $config = Config::getConfigurationValues('plugin:AssistIA');
        $server_url = $config['server_url'] ?? '';
        $enabled = $config['enabled'] ?? 0;
        $timeout = $config['timeout'] ?? 10;

        echo "<form name='form' action=\"" . $_SERVER['PHP_SELF'] . "\" method='post'>";
        echo "<div class='center' id='tabsbody'>";
        echo "<table class='tab_cadre_fixe'>";
        
        echo "<tr><th colspan='2'>" . __('Configuración AssistIA', 'glpiassistia') . '</th></tr>';
        
        // Campo para habilitar/deshabilitar el plugin
        echo "<tr class='tab_bg_1'>";
        echo "<td>" . __('Habilitar AssistIA', 'glpiassistia') . "</td>";
        echo "<td>";
        echo "<input type='hidden' name='config_class' value='PluginGlpiassistiaConfig'>";
        Dropdown::showYesNo('enabled', $enabled);
        echo "</td></tr>";
        
        // Campo URL del servidor
        echo "<tr class='tab_bg_1'>";
        echo "<td>" . __('URL del servidor AssistIA', 'glpiassistia') . "</td>";
        echo "<td>";
        echo "<input type='url' name='server_url' size='80' value='" . 
             Html::cleanInputText($server_url) . "' placeholder='http://localhost:8000/api/tickets'>";
        echo "<br><small>" . __('Ejemplo: http://servidor.com:8000/api/tickets', 'glpiassistia') . "</small>";
        echo "</td></tr>";
        
        // Campo timeout
        echo "<tr class='tab_bg_1'>";
        echo "<td>" . __('Timeout de conexión (segundos)', 'glpiassistia') . "</td>";
        echo "<td>";
        echo "<input type='number' name='timeout' min='1' max='60' value='$timeout'>";
        echo "<br><small>" . __('Tiempo máximo de espera para la conexión (1-60 segundos)', 'glpiassistia') . "</small>";
        echo "</td></tr>";

        // Botón de prueba de conexión
        echo "<tr class='tab_bg_1'>";
        echo "<td colspan='2' class='center'>";
        if (!empty($server_url)) {
            echo "<button type='button' class='btn btn-info' onclick='testAssistIAConnection()'>";
            echo __('Probar conexión', 'glpiassistia') . "</button>&nbsp;";
        }
        echo "</td></tr>";

        echo "<tr class='tab_bg_2'>";
        echo "<td colspan='2' class='center'>";
        echo "<input type='submit' name='update' class='btn btn-primary' value=\"" . 
             _sx('button', 'Guardar') . '">';
        echo "</td></tr>";

        echo "</table></div>";
        Html::closeForm();

        // JavaScript para prueba de conexión
        if (!empty($server_url)) {
            echo "<script>
            function testAssistIAConnection() {
                const configUrl = '" . Html::cleanInputText($server_url) . "';
                
                // Si la URL termina en /run-agent, usar la URL base para el test
                let testUrl = configUrl;
                if (configUrl.endsWith('/run-agent')) {
                    testUrl = configUrl.replace('/run-agent', '/health');
                } else if (configUrl.endsWith('/')) {
                    testUrl = configUrl + 'health';
                } else {
                    testUrl = configUrl + '/health';
                }
                
                const testData = {
                    id: 0,
                    title: 'Test de conexión desde GLPI',
                    description: 'Esta es una prueba de conexión desde GLPI AssistIA'
                };
                
                console.log('URL configurada:', configUrl);
                console.log('URL para test:', testUrl);
                console.log('Datos de test:', testData);
                
                fetch(testUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(testData)
                })
                .then(response => {
                    console.log('Response status:', response.status);
                    
                    return response.text().then(text => {
                        console.log('Response text:', text);
                        
                        let data;
                        try {
                            data = text ? JSON.parse(text) : {};
                        } catch (e) {
                            console.error('JSON parse error:', e);
                            data = { raw_response: text };
                        }
                        
                        return {
                            status: response.status,
                            data: data,
                            raw: text
                        };
                    });
                })
                .then(result => {
                    console.log('Processed response:', result);
                    
                    if (result.status >= 200 && result.status < 300) {
                        if (result.data.status === 'ok') {
                            alert('✅ ' + (result.data.message || 'Conexión exitosa'));
                        } else if (result.raw) {
                            alert('✅ Servidor respondiendo. Respuesta: ' + result.raw.substring(0, 100));
                        } else {
                            alert('✅ Conexión exitosa (respuesta vacía)');
                        }
                    } else if (result.status === 405) {
                        alert('⚠️ Método no permitido. El servidor está funcionando pero no acepta POST en ' + testUrl + '\\n\\nIntenta configurar la URL como: ' + configUrl.replace('/run-agent', ''));
                    } else {
                        const errorMsg = result.data.message || result.raw || 'Sin respuesta del servidor';
                        alert('⚠️ Error HTTP ' + result.status + ': ' + errorMsg);
                    }
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                    if (error.message.includes('Failed to fetch')) {
                        alert('❌ No se pudo conectar al servidor. \\n\\nVerifica que esté corriendo en: ' + testUrl + '\\n\\nSi estás usando Docker, prueba con: http://host.docker.internal:8089/run-agent');
                    } else {
                        alert('❌ Error: ' + error.message);
                    }
                });
            }
            </script>";
        }

        return true;
    }
}