# Parte 1 — SequentialAgent: flujo lineal de investigación y escritura

Esta parte introduce los **agentes de flujo de trabajo** (`workflow agents`) mediante un `SequentialAgent` que ejecuta sus sub-agentes uno tras otro, en un orden fijo.

## Idea general

El usuario pide una película sobre un personaje histórico. Un agente `greeter` recibe la solicitud, almacena el tema en el estado de sesión y transfiere el control a un equipo secuencial que:

1. **researcher** — busca información en Wikipedia sobre el personaje indicado.
2. **screenwriter** — escribe un logline y un esquema de tres actos basándose en la investigación.
3. **file_writer** — genera un título comercial y guarda el pitch en un archivo `.txt`.

```text
Usuario
  │
  ▼
greeter  ──► film_concept_team (SequentialAgent)
                 │
                 ├─ 1. researcher       (Wikipedia + append_to_state)
                 ├─ 2. screenwriter     (append_to_state)
                 └─ 3. file_writer      (write_file)
```

## Conceptos clave

| Concepto | Descripción |
| --- | --- |
| `SequentialAgent` | Ejecuta sub-agentes en el orden definido, sin intervención del usuario entre pasos |
| `LangchainTool` | Envuelve la herramienta `WikipediaQueryRun` de LangChain para usarla en ADK |
| `append_to_state` | Herramienta que acumula texto en el diccionario de estado de la sesión |
| `write_file` | Herramienta que crea un archivo en disco con el contenido generado |
| Estado de sesión | Se usa `{ PROMPT? }`, `{ PLOT_OUTLINE? }`, etc. para compartir datos entre agentes |

## Diferencia con las otras partes

Esta parte realiza **una única pasada**: investigar → escribir → guardar. No existe un agente crítico ni un ciclo de mejora. Las partes 2 y 3 amplían este flujo añadiendo iteración y paralelismo.

## Archivos

- `workflow_agents/agent.py` — definición de agentes, herramientas y flujo.
- `workflow_agents/__init__.py` — permite a ADK descubrir el paquete.
- `workflow_agents/.env` — variables de entorno (no versionado).

## Ejecución

```bash
cd multiagent_systems
adk run parte_1_sequential/workflow_agents
```

