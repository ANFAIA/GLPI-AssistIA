# GLPI AssistIA
This README is available in multiple languages: [Español](README.md) | [Galego](README.gl.md) | [English](README.en.md)

## 🎯 Use Case

Incident management, especially in IT departments, often involves repetitive tasks such as checking Wikis, documentation, or executing commands like *Ping* to certain servers. GLPI AssistIA aims to reduce this workload with a preliminary incident report. Once an incident is registered in the system, it is sent to a server (GLPI AssistIA Server) which generates a report with possible solutions. This report will be visible to the agent handling the incident as a private note at the moment they take on the case, thus reducing response times.

## 🏗️ Architecture and Overview
The system’s core is designed around a workflow that is triggered by the creation of a ticket in GLPI. The ticket information is processed by an intelligent agent system (`CrewAI`) that collaborates to analyze, enrich, and propose solutions.

This `CrewAI` connects to external tools (knowledge bases, monitoring systems) through an **MCP Server (Model Context Protocol)**, which acts as a data bus.

### Ticket Workflow
![Architecture Diagram V3](https://raw.githubusercontent.com/ANFAIA/GLPI-AssistIA/b0f1cb55bdc569c4f83b0b36e34c96536fe1d644/docs/BigPicture_VersionActual.svg)

1. **Entry in GLPI**: A user or technician creates an incident ticket.
2. **Agent Activation**: The incident is transferred to the `CrewAI` system hosted in GLPI AssistIA Server for processing.
3. **AI Agent Analysis**:
   * **Emotion Analyst**: Evaluates the urgency and mood of the user to prioritize the ticket.
   * **Categorizer Agent**: Classifies the incident according to predefined GLPI tags.
   * **Resolver Agent**: Reviews available data in Wiki.js, past GLPI incidents, and performs *Pings* (in case of connection issues). Finally, it consolidates all the information, generates an enriched summary, and proposes a possible solution.
4. **Response in GLPI**: The generated solution and analysis are published in the GLPI ticket, assisting the technician or responding directly to the user.

## ✨ Key Features

* **Ticket Summarization and Enrichment**: The AI analyzes and summarizes the user’s problem, adding technical context.
* **MCP Architecture**: A decoupled data bus to facilitate communication and scalability.
* **Smart Contextual Information**: Provides relevant information to both technicians and users.

## Requirements
- **GLPI** version 10.x or higher (API access).
- **GLPI Credentials:** `GLPI_URL`, `GLPI_APP_TOKEN`, and `GLPI_USER_TOKEN`.
- **AssistIA Server** (`glpiassistiaserver/`):
  - If **PHP**, requires **PHP ≥ 8.1** and **Composer**.
  - If **Python**, requires **Python ≥ 3.11**.
- **MCP (optional but recommended):** `python ≥ 3.11` to run `mcp_server.py`.
- **(Optional)** Local LLM if orchestration uses local models (e.g., Ollama).

## Environment Variables
Create a `.env` file containing:

```env
# GLPI
GLPI_URL=https://your-glpi.example.com
GLPI_API_URL=https://my.glpi/apirest.php
GLPI_APP_TOKEN=xxx
GLPI_USER_TOKEN=yyy
GLPI_VERIFY_SSL=true

# MCP
MCP_HOST=127.0.0.1
MCP_PORT=8765

# LLM Provider (Enter one line)
OLLAMA_HOST=[OLLAMA HOST]
CEREBRAS_API_KEY=[API KEY]
GROQ_API_KEY=[API KEY]

# Wiki.js
WIKIJS_URL=http://localhost:8080/
WIKIJS_API_TOKEN=your_token
```

## Getting Started
### Server
The system consists of two servers. The first is WebApp, which will receive incidents. You can start it with the following command from the repository’s root directory:  
```bash
uvicorn glpiassistiaserver.webapp:app --host 0.0.0.0 --port 8089 --reload
```

The second is MCP Server, which will handle communications between GLPI AssistIA Server and the tools. You can start it by running the `mcp_server.py` script directly (if you want to change some parameters, you can use the `uvicorn` command as in the previous step).

### Plugin Installation
You need to move the `glpiassistia` folder to your GLPI plugins directory and install it. Once installed, go to configuration, enable the GLPI AssistIA option, set the GLPI AssistIA Server address, and save the data. After these steps, enable the plugin in the plugins section. Each time an incident is created, it will be sent to the server.

## Screenshots
### Practical Cases
Below is an example of incident processing:

<img width="475.25" height="226.75" alt="INCIDENT OPENING" src="https://github.com/user-attachments/assets/06465e4f-4ed0-4f21-8a60-67f224985b2a" />
<img width="421.25" height="196.5" alt="PROCESSING" src="https://github.com/user-attachments/assets/2547cee4-0c46-48ef-a622-03cb887ab306" />

<img width="475.5" height="228" alt="RES" src="https://github.com/user-attachments/assets/cbfadd07-f0a8-4314-9fbb-fb51cc9aae94" />
<img width="475.75" height="228" alt="RES2" src="https://github.com/user-attachments/assets/b2a81c28-b1f1-43b0-a075-8c82ee3dcdc6" />

### Plugin
Below is the plugin interface:

<img width="475.5" height="226.75" alt="CONFIGURATION" src="https://github.com/user-attachments/assets/58d67305-c90a-48a0-8980-1af7b5af24fa" />

## Quick Setup Video and Practical Example
The following video shows the plugin configuration and a usage example:  
[![GLPIASSISTIA](https://img.youtube.com/vi/dWSrIz5tcgw/0.jpg)](https://www.youtube.com/watch?v=dWSrIz5tcgw)


## 📊 Success Metrics

The project’s success will be measured by achieving the following objectives:

* Reduction of more than **70%** in first response time.
* Accuracy above **85%** in automatically generated responses.
* Reduction of more than **50%** in tickets requiring manual escalation.
* Reduction of more than **40%** in average incident resolution time.
* User satisfaction level above **4.0/5.0**.

---

## 🤝 Collaboration
This project was made possible thanks to the ANFAIA Summer Scholarship program and the collaboration of Aitire.