# Parent and Subagents — Transferencias entre agente padre y sub-agentes

Este sub-proyecto es compartido por las tres partes del laboratorio. Demuestra cómo un agente raíz (`root_agent`) puede transferir el control de la conversación hacia sub-agentes especializados, basándose en la intención del usuario.

## Idea general

El agente raíz, llamado `steering`, saluda al usuario y le pregunta si ya sabe a qué país quiere viajar o si necesita ayuda para decidirse. Según la respuesta, el control pasa a uno de sus dos sub-agentes:

- **travel_brainstormer** — sugiere países según las prioridades del viajero (aventura, ocio, aprendizaje, compras o arte).
- **attractions_planner** — propone atracciones dentro del país elegido y las guarda en el estado de sesión usando la herramienta `save_attractions_to_state`.

```text
Usuario
  │
  ▼
steering (root_agent)
  │
  ├─ "No sé a dónde ir" ──► travel_brainstormer
  │
  └─ "Quiero ir a Japón" ──► attractions_planner
                                    │
                                    └─ save_attractions_to_state (tool)
```

## Conceptos clave

| Concepto | Descripción |
| --- | --- |
| `sub_agents` | Parámetro del agente padre que define qué agentes están disponibles para recibir transferencias |
| `description` | Cada sub-agente describe su función; el padre las lee para decidir a quién transferir |
| `instruction` | Las instrucciones del padre mencionan a los sub-agentes por nombre para guiar la transferencia |
| `ToolContext.state` | Diccionario compartido en la sesión donde `attractions_planner` acumula la lista de atracciones |
| `before_model_callback` / `after_model_callback` | Callbacks de logging que registran las consultas enviadas al modelo y sus respuestas |

## Transferencia implícita vs. explícita

El agente padre no necesita lógica personalizada para transferir: ADK se encarga de evaluar las descripciones de los sub-agentes y decidir cuál es más adecuado. Las instrucciones del padre refuerzan esa decisión mencionando nombres concretos:

> *"If they need help deciding, send them to 'travel_brainstormer'."*

## Archivos

- `agent.py` — definición de los tres agentes, la herramienta de estado y el plugin 429.
- `__init__.py` — permite a ADK descubrir el paquete.
- `.env` — variables de entorno (no versionado).

## Ejecución

```bash
cd build_multi_agent_systems_with_adk
adk run parent_and_subagents
```

Luego, prueba estas interacciones:

| Entrada del usuario | Comportamiento esperado |
| --- | --- |
| `hello` | El agente `steering` pregunta si ya tiene destino o necesita ayuda |
| `I need help deciding` | Transfiere a `travel_brainstormer`, que sugiere países |
| `I want to visit Japan` | Transfiere a `attractions_planner`, que propone atracciones |
| `Add the temples` | `attractions_planner` llama a `save_attractions_to_state` |
| `Show my list` | Muestra las atracciones acumuladas en `{ attractions? }` |

