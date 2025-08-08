# Instalación de GLPI en local y breve análisis
Para poner en contexto el desarrollo del plugin y probar tanto el programa como el plugin, se ha procedido a realizar una instalación local de GLPI mediante Docker. A continuación se exponen unos matices y anotaciones a tener en cuenta.
## Instalación de Docker
Para poder ejecutar GLPI en LocalHost debemos instalar Docker, este creara unos contenedores en nuestro eqípo que nos permitrán hacer servidores locales que emplean un kernel de Linux.
Una vez instalemos docker debemos de crear un archivo **docker-compose.yml** con la siguiente estructura:

```yaml
version: '3.8'

services:
  db:
    image: mariadb:10.6
    container_name: glpi-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: [Una contraseña de root]
      MYSQL_DATABASE: [Un nombre de base de datos]
      MYSQL_USER: [Un usuario de acceso a la base de datos]
      MYSQL_PASSWORD: [Una contraseña de acceso a la base de datos]
    volumes:
      - db_data:/var/lib/mysql

  glpi:
    image: diouxx/glpi
    container_name: glpi-web
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      TIMEZONE: Europe/Madrid
    volumes:
      - glpi_data:/var/www/html

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: glpi-phpmyadmin
    restart: always
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      MYSQL_ROOT_PASSWORD: [Una contraseña de acceso root a la base de datos]

volumes:
  db_data:
  glpi_data:
```


Ejecutando este archivo se nos crearan los contenedores necesarios y podremos configurar el servidor GLPI mediante su interfaz gráfica.

## Puntos fuertes de GLPI y posibles integraciones
La idea del plugin es que se ejecute mediante un trigger. Cuando sea llamado, este deberá de dar pistas, analizar los ánimos del cliente (Darle prioridad o escalar si ya ha preguntado varias veces o esta enfadado), dar un resumen de su historial... para agilizar y mejorar el servicio al cliente. Este sistema se puede dividir en agentes con el objetivo de que cada uno mire una caracteristica.
GLPI cuenta con un sistema de gestión de activos nativo, por lo que integrarlo con otros servicios como Wiki.js, Wazuh o Zabbix sería de gran relevancia. El plugin se podría comunicar con GLPI mediante MCP.