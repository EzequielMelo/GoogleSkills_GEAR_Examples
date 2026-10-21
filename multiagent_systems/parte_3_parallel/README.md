# Parte 3 — ParallelAgent: preproducción en paralelo

Esta parte es la versión completa del laboratorio. Sobre el flujo iterativo de la Parte 2, se añade un **equipo de preproducción** que trabaja en paralelo: mientras un agente analiza el potencial de taquilla, otro genera ideas de casting. Ambos resultados se incorporan al documento final.

## Idea general

Una vez que el `writers_room` (LoopAgent) produce un guión pulido, un `ParallelAgent` ejecuta simultáneamente dos agentes de análisis. Finalmente, el `file_writer` combina el guión, el informe de taquilla y el casting en un único documento.

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
                 ├─ 2. preproduction_team (ParallelAgent)
                 │       │
                 │       ├─ box_office_researcher  (output_key → box_office_report)
                 │       └─ casting_agent          (output_key → casting_report)
                 │
                 └─ 3. file_writer          (write_file)
```

## Conceptos clave

| Concepto | Descripción |
| --- | --- |
| `ParallelAgent` | Ejecuta todos sus sub-agentes al mismo tiempo, sin orden fijo |
| `output_key` | Parámetro que guarda la respuesta de un agente en una clave del estado de sesión |
| `box_office_researcher` | Agente que analiza el potencial comercial comparándolo con películas recientes |
| `casting_agent` | Agente que sugiere actores basándose en roles similares |

## Diferencia con las otras partes

Respecto a la Parte 2, se añade:
- Un **ParallelAgent** (`preproduction_team`) con dos sub-agentes que trabajan simultáneamente.
- Los agentes paralelos usan `output_key` para escribir sus resultados en el estado, que luego el `file_writer` lee mediante `{ box_office_report? }` y `{ casting_report? }`.
- El `file_writer` ahora combina tres fuentes: guión, taquilla y casting.

## Archivos

- `workflow_agents/agent.py` — definición completa con `LoopAgent` + `ParallelAgent`.
- `workflow_agents/__init__.py` — permite a ADK descubrir el paquete.
- `workflow_agents/.env` — variables de entorno (no versionado).

## Ejecución

```bash
cd multiagent_systems
adk run parte_3_parallel/workflow_agents
```

