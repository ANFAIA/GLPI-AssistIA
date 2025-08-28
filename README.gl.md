# GLPI AssistIA
Este README está dispoñible en varios idiomas: [Español](README.md) | [Galego](README.gl.md) | [English](README.en.md)

## 🎯 Caso de uso

A xestión de incidencias, especialmente en departamentos de IT, require tarefas que moitas veces son repetitivas como revisar Wikis, documentación ou a execución de comandos como *Ping* a determinados servidores. GLPI AssistIA busca reducir toda esta carga cun informe previo da incidencia a tratar. Unha vez se rexistra unha incidencia no sistema, esta envíase a un servidor (GLPI AssistIA Server) que xera un informe con posibles solucións. Este informe estará dispoñible para o axente que trate a incidencia como unha nota privada no momento de asumir o caso, reducindo así os tempos de resposta.

## 🏗️ Arquitectura e Visión Xeral
O núcleo do sistema está deseñado arredor dun fluxo de traballo que se activa coa creación dun ticket en GLPI. A información do ticket é procesada por un sistema de axentes intelixentes (`CrewAI`) que colaboran para analizar, enriquecer e propoñer solucións.

Este `CrewAI` conéctase a ferramentas externas (bases de coñecemento, sistemas de monitorización) a través dun **Servidor MCP (Model Context Protocol)**, que actúa como un bus de datos.

### Fluxo de Traballo do Ticket
![Diagrama de Arquitectura V3](https://raw.githubusercontent.com/ANFAIA/GLPI-AssistIA/c81ce359886bd2f5c9111d7a7446144947432ea3/docs/BigPicture%20V3.svg)

1.  **Entrada en GLPI**: Un usuario ou técnico crea un ticket de incidencia.
2.  **Activación do Axente**: A incidencia transfírese ao sistema `CrewAI` aloxado en GLPI AssistIA Server para o seu procesamento.
3.  **Análise por Axentes IA**:
      * **Analista de Emocións**: Avalía a urxencia e o estado de ánimo do usuario para priorizar o ticket.
      * **Axente Categorizador**: Clasifica a incidencia segundo as etiquetas predefinidas en GLPI.
      * **Axente Resolutor**: Revisa os datos dispoñibles en Wiki.js, incidencias anteriores de GLPI e realiza *Pings* (no caso de problemas de conexión). Finalmente consolida toda a información, xera un resumo enriquecido e unha posible solución.
4.  **Resposta en GLPI**: A solución e a análise xeradas publícanse no ticket de GLPI, asistindo ao técnico ou respondendo directamente ao usuario.

## ✨ Características Principais

  * **Resumo e Enriquecemento de Tickets**: A IA analiza e resume o problema do usuario, engadindo contexto técnico.
  * **Arquitectura MCP**: Un bus de datos desacoplado para facilitar a comunicación e a escalabilidade.
  * **Información Contextual Intelixente**: Fornece información relevante tanto a técnicos como a usuarios.

## Requisitos
- **GLPI** versión 10.x ou superior (acceso vía API).
- **Credenciais GLPI:** `GLPI_URL`, `GLPI_APP_TOKEN` e `GLPI_USER_TOKEN`.
- **Servidor AssistIA** (`glpiassistiaserver/`):
  - Se é **PHP**, require **PHP ≥ 8.1** e **Composer**.
  - Se é **Python**, require **Python ≥ 3.11**.
- **MCP (opcional pero recomendado):** `python ≥ 3.11` para executar `mcp_server.py`.
- **(Opcional)** LLM local se a orquestración usa modelos locais (por exemplo, Ollama).

## Variables de contorno
Crea un ficheiro `.env` que conteña:

```env
# GLPI
GLPI_URL=https://teu-glpi.example.com
GLPI_API_URL=https://meu.glpi/apirest.php
GLPI_APP_TOKEN=xxx
GLPI_USER_TOKEN=yyy
GLPI_VERIFY_SSL=true

# MCP
MCP_HOST=127.0.0.1
MCP_PORT=8765

# Provedor de LLM (Introduce unha liña)
OLLAMA_HOST=[HOST DE OLLAMA]
CEREBRAS_API_KEY=[API KEY]
GROQ_API_KEY=[API KEY]

# Wiki.js
WIKIJS_URL=http://localhost:8080/
WIKIJS_API_TOKEN=teu_token
```

## Poñer en marcha
### Servidor
O sistema consta de dous servidores, o primeiro é WebApp que recibirá as incidencias. Pódese iniciar co seguinte comando desde o directorio principal do repositorio:  
```bash
uvicorn glpiassistiaserver.webapp:app --host 0.0.0.0 --port 8089 --reload
```

O segundo é MCP Server, que realizará as comunicacións entre GLPI AssistIA Server e as ferramentas. Pódese iniciar executando directamente o script `mcp_server.py` (se desexas cambiar algún dato podes usar o comando `uvicorn` como fixemos no paso anterior).

### Instalación do plugin
Deberás mover o cartafol `glpiassistia` ao cartafol de plugins do teu GLPI e instalalo. Unha vez instalado, deberás entrar en configuración, activar a opción de GLPI AssistIA, establecer o enderezo de GLPI AssistIA Server e gardar os datos. Despois destes pasos, deberás activar o plugin no apartado de plugins. Cada vez que se cree unha incidencia será enviada ao servidor.

## Capturas de Pantalla
### Casos prácticos
A continuación móstrase o procesamento dunha incidencia de exemplo:

<img width="475.25" height="226.75" alt="APERTURA INCIDENCIA" src="https://github.com/user-attachments/assets/06465e4f-4ed0-4f21-8a60-67f224985b2a" />
<img width="421.25" height="196.5" alt="PROCESAMENTO" src="https://github.com/user-attachments/assets/2547cee4-0c46-48ef-a622-03cb887ab306" />

<img width="475.5" height="228" alt="RES" src="https://github.com/user-attachments/assets/cbfadd07-f0a8-4314-9fbb-fb51cc9aae94" />
<img width="475.75" height="228" alt="RES2" src="https://github.com/user-attachments/assets/b2a81c28-b1f1-43b0-a075-8c82ee3dcdc6" />

### Plugin
A continuación móstrase a interface do plugin:

<img width="475.5" height="226.75" alt="CONFIGURACION" src="https://github.com/user-attachments/assets/58d67305-c90a-48a0-8980-1af7b5af24fa" />

## Vídeo de configuración rápida e exemplo práctico
No seguinte vídeo móstrase a configuración do plugin e un exemplo de uso:  
[![GLPIASSISTIA](https://img.youtube.com/vi/Me0OWoNrdao/0.jpg)](https://www.youtube.com/watch?v=Me0OWoNrdao)

## 📊 Métricas de Éxito

O éxito do proxecto medirase pola consecución dos seguintes obxectivos:

  * Redución de máis do **70%** no tempo de primeira resposta.
  * Precisión superior ao **85%** nas respostas automáticas xeradas.
  * Redución de máis do **50%** nos tickets que precisan ser escalados manualmente.
  * Redución de máis do **40%** no tempo medio de resolución de incidencias.
  * Nivel de satisfacción do usuario superior a **4.0/5.0**.

---

## 🤝 Colaboración
Este proxecto foi posíbel grazas ao programa de Bolsas de Verán de ANFAIA e á colaboración de Aitire.
