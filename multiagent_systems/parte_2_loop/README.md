# Parte 2 — LoopAgent: ciclo iterativo de mejora

Esta parte extiende el flujo secuencial de la Parte 1 añadiendo un **ciclo de retroalimentación** mediante un `LoopAgent`. El guión se investiga, se escribe, se critica y se mejora varias veces antes de guardarse.

## Idea general

El flujo ahora introduce un agente `critic` que evalúa el esquema de la película. Si el guión necesita mejoras, el crítico registra su feedback y el ciclo vuelve a empezar (investigar → escribir → criticar). Cuando el crítico queda satisfecho, llama a `exit_loop` para salir del ciclo.

```text
Usuario
  │
  ▼
greeter  ──► film_concept_team (SequentialAgent)
                 │
                 ├─ 1. writers_room (LoopAgent, max 5 iteraciones)
                 │       │
                 │       ├─ researcher       (Wikipedia + append_to_state)
                 │       ├─ screenwriter     (append_to_state)
                 │       └─ critic           (append_to_state + exit_loop)
                 │
                 └─ 2. file_writer          (write_file)
```

## Conceptos clave

| Concepto | Descripción |
| --- | --- |
| `LoopAgent` | Ejecuta sus sub-agentes en ciclo hasta que uno llame a `exit_loop` o se alcance `max_iterations` |
| `exit_loop` | Herramienta incorporada de ADK que detiene la iteración del `LoopAgent` |
| `critic` | Agente que evalúa la calidad del guión y decide si continuar mejorando o finalizar |
| `CRITICAL_FEEDBACK` | Clave de estado donde el crítico almacena sugerencias para la siguiente iteración |

## Diferencia con las otras partes

Respecto a la Parte 1, se añade:
- Un agente **critic** que evalúa el resultado.
- Un **LoopAgent** (`writers_room`) que itera el ciclo investigar → escribir → criticar.
- La herramienta `exit_loop` para que el crítico controle cuándo el guión es suficientemente bueno.

La Parte 3 amplía este flujo añadiendo además un `ParallelAgent`.

## Archivos

- `workflow_agents/agent.py` — definición de agentes, herramientas y flujo con `LoopAgent`.
- `workflow_agents/__init__.py` — permite a ADK descubrir el paquete.
- `workflow_agents/.env` — variables de entorno (no versionado).

## Ejecución

```bash
cd multiagent_systems
adk run parte_2_loop/workflow_agents
```

