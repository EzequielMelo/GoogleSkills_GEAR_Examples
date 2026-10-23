# Ejercicios de Gemini Agents con Google ADK

Este repositorio reúne pequeños proyectos creados durante un curso de agentes con Gemini y Google Agent Development Kit (ADK). Cada carpeta es un ejercicio independiente y se concentra en un concepto concreto.

## Proyectos

| Proyecto | Tema principal |
| --- | --- |
| [`my_first_agent`](./my_first_agent/) | Creación y configuración básica de un primer agente |
| [`product_extractor`](./product_extractor/) | Salidas JSON estructuradas mediante un esquema de Pydantic |
| [`name_extractor`](./name_extractor/) | Uso de `output_key` y estado de sesión |
| [`model_comparison`](./model_comparison/) | Comparación de modelos y configuración de generación |
| [`problem_solver`](./problem_solver/) | Planificación y razonamiento de varios pasos con `BuiltInPlanner` |
| [`personalized_greeter`](./personalized_greeter/) | Personalización de instrucciones mediante el estado de sesión |
| [`namespace_demo`](./namespace_demo/) | Alcance y persistencia de los namespaces de estado |
| [`geography_assistant`](./geography_assistant/) | Uso de una función de Python como herramienta para consultar capitales |
| [`research_assistant`](./research_assistant/) | Búsqueda de Google integrada para investigar información actual |
| [`math_assistant`](./math_assistant/) | Ejecución de código integrada para cálculos matemáticos |
| [`file_reader_assistant`](./file_reader_assistant/) | Lectura de archivos mediante un servidor MCP local |
| [`travel_agent`](./travel_agent/) | Coordinación de varias herramientas de función personalizadas |
| [`customer_support`](./customer_support/) | Instrucciones estratégicas, manejo de errores y derivación de casos |
| [`build_multi_agent_systems_with_adk`](./build_multi_agent_systems_with_adk/) | Build Multi-Agent Systems with ADK: transferencias padre/sub-agente, `SequentialAgent`, `LoopAgent` y `ParallelAgent` |
| [`connect_to_remote_agents_with_adk_and_a2a`](./connect_to_remote_agents_with_adk_and_a2a/) | Connect to Remote Agents with ADK and A2A: servidores A2A en Cloud Run, Agent Cards y `RemoteA2aAgent` |
| [`use_mcp_tools_with_adk_agents`](./use_mcp_tools_with_adk_agents/) | Use Model Context Protocol (MCP) Tools with ADK Agents: cliente de servidores MCP remotos (Google Maps) y servidor MCP custom con herramientas ADK |

### Detalle de `build_multi_agent_systems_with_adk` (Build Multi-Agent Systems with ADK)

El proyecto proviene del laboratorio **"Build Multi-Agent Systems with ADK"** del programa GEAR (Gemini Enterprise Agent Ready) de Google. Se divide en un módulo compartido y tres partes progresivas:

| Sub-proyecto | Tema |
| --- | --- |
| [`parent_and_subagents`](./build_multi_agent_systems_with_adk/parent_and_subagents/) | Transferencias entre agente padre y sub-agentes según la intención del usuario |
| [`parte_1_sequential`](./build_multi_agent_systems_with_adk/parte_1_sequential/) | `SequentialAgent` — flujo lineal: investigar → escribir → guardar |
| [`parte_2_loop`](./build_multi_agent_systems_with_adk/parte_2_loop/) | `LoopAgent` — ciclo iterativo de investigación, escritura y crítica |
| [`parte_3_parallel`](./build_multi_agent_systems_with_adk/parte_3_parallel/) | `ParallelAgent` — preproducción en paralelo (taquilla + casting) |

### Detalle de `connect_to_remote_agents_with_adk_and_a2a` (Connect to Remote Agents with ADK and the Agent2Agent SDK)

El proyecto proviene del laboratorio **"Connect to Remote Agents with ADK and the Agent2Agent (A2A) SDK"** (GENAI120) del programa GEAR. Demuestra cómo conectar agentes remotos como microservicios independientes mediante el protocolo Agent2Agent:

| Sub-agente | Rol |
| --- | --- |
| [`illustration_agent`](./connect_to_remote_agents_with_adk_and_a2a/illustration_agent/) | Servidor A2A desplegado en Cloud Run que genera ilustraciones corporativas y las sube a Google Cloud Storage |
| [`slide_content_agent`](./connect_to_remote_agents_with_adk_and_a2a/slide_content_agent/) | Cliente ADK que redacta contenido para diapositivas y delega la ilustración al agente remoto mediante `RemoteA2aAgent` y su Agent Card |

### Detalle de `use_mcp_tools_with_adk_agents` (Use Model Context Protocol Tools with ADK Agents)

El proyecto proviene del laboratorio **"Use Model Context Protocol (MCP) Tools with ADK Agents"** (GENAI124) del programa GEAR. Demuestra los dos patrones de integración de MCP con Google ADK:

| Módulo / Agente | Rol y Patrón MCP |
| --- | --- |
| [`google_maps_mcp_agent`](./use_mcp_tools_with_adk_agents/google_maps_mcp_agent/) | **Patrón 1 (ADK como Cliente MCP):** Consume el servidor MCP remoto de Google Maps (*Maps Grounding Lite*) mediante `MCPToolset` y Streamable HTTP con autenticación OAuth |
| [`adk_mcp_server`](./use_mcp_tools_with_adk_agents/adk_mcp_server/) | **Patrón 2 (Servidor MCP con herramientas ADK):** Implementa un servidor MCP (`adk_server.py`) que expone `load_web_page` vía `stdio`, consumido por un agente ADK cliente |

Cada proyecto contiene su propio `README.md` con una explicación del código y formas de probarlo.

## Configuración general

Los ejercicios requieren Python, Google ADK y una clave para acceder al modelo de Gemini. Las credenciales deben guardarse en archivos `.env` locales. Estos archivos están excluidos de Git para evitar publicar secretos accidentalmente.

Ejemplo orientativo:

```env
GOOGLE_API_KEY=tu_clave
```

No incluyas claves reales en commits ni en archivos de ejemplo.
