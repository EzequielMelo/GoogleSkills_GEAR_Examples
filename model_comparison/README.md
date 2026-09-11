# Model Comparison

Este proyecto compara agentes configurados para tareas diferentes. En lugar de aplicar los mismos parámetros a todos los casos, cada agente se optimiza según su objetivo: extraer hechos con consistencia o generar ideas con mayor variedad.

## Conceptos practicados

- Uso de distintos modelos de Gemini según la tarea.
- Configuración de `GenerateContentConfig` desde `google.genai.types`.
- Control de la variabilidad mediante `temperature`, `top_p` y `top_k`.
- Limitación de la respuesta con `max_output_tokens`.
- Configuración de filtros mediante `SafetySetting`.
- Consulta de los modelos habilitados para `generateContent`.

## Temperatura

La temperatura modifica cuánta variación permite el modelo al generar una respuesta. Como guía práctica utilizada en este ejercicio:

| Rango | Comportamiento esperado | Ejemplos de uso |
| --- | --- | --- |
| `0.0–0.3` | Más fáctico y consistente | Extracción de datos, clasificación y respuestas precisas |
| `0.4–0.7` | Equilibrio entre consistencia y variedad | Explicaciones, asistentes generales y redacción |
| `0.8–1.0` | Más diverso y creativo | Lluvia de ideas, historias y exploración de alternativas |

Una temperatura baja no garantiza que una respuesta sea verdadera; reduce la variabilidad. La exactitud también depende de las instrucciones, el contexto, el modelo y la validación de los resultados.

## Agentes incluidos

### Agente fáctico

`factual_agent` utiliza una temperatura de `0.1` y un límite de 500 tokens. Sus instrucciones evitan inferencias, suposiciones y lenguaje creativo. También emplea valores más restrictivos de `top_p` y `top_k` para favorecer respuestas concentradas y consistentes.

### Agente creativo

`creative_agent` utiliza una temperatura de `0.9`, permite hasta 2000 tokens y amplía `top_p` y `top_k`. Esto favorece respuestas variadas y detalladas para sesiones de lluvia de ideas.

La variable `root_agent` determina cuál de los dos se abre en ADK. Actualmente apunta a:

```python
root_agent = creative_agent
```

Puedes cambiarla a `factual_agent` para comparar el comportamiento usando una misma entrada.

## `GenerateContentConfig`

El proyecto importa los tipos de configuración así:

```python
from google.genai import types
```

Después, cada agente recibe una instancia de:

```python
types.GenerateContentConfig(
    temperature=0.1,
    max_output_tokens=500,
    top_p=0.8,
    top_k=10,
    safety_settings=[...],
)
```

- `temperature`: regula la variabilidad de la generación.
- `max_output_tokens`: establece la longitud máxima de la respuesta.
- `top_p`: limita la selección a un conjunto acumulado de tokens probables.
- `top_k`: limita la selección a una cantidad de candidatos probables.
- `safety_settings`: define categorías de riesgo y sus umbrales de bloqueo.

`temperature`, `top_p` y `top_k` interactúan entre sí. Conviene modificarlos de forma intencional y comparar los resultados, en lugar de asumir que una única configuración sirve para cualquier tarea.

## Umbrales de seguridad

Cada `SafetySetting` combina una categoría de contenido con un umbral. Entre los valores disponibles, `BLOCK_LOW_AND_ABOVE` aplica un bloqueo más estricto, mientras que `BLOCK_ONLY_HIGH` bloquea únicamente el nivel de probabilidad más alto y es más flexible. También existen opciones intermedias, como `BLOCK_MEDIUM_AND_ABOVE`.

En este ejercicio:

- El agente fáctico usa `BLOCK_LOW_AND_ABOVE` para contenido peligroso.
- El agente creativo usa `BLOCK_MEDIUM_AND_ABOVE` para la misma categoría.

Una configuración más flexible no significa que el contenido sea seguro por defecto. Los umbrales deben elegirse considerando el público, el dominio y el riesgo de la aplicación.

## Archivos

- `agent.py`: define los agentes fáctico y creativo con sus respectivas configuraciones.
- `list_models.py`: consulta la API e imprime los modelos habilitados para `generateContent`.
- `__init__.py`: expone el módulo del agente como paquete de Python.

## Ejecución

Para abrir el agente seleccionado como `root_agent`, ejecuta desde la carpeta que contiene todos los proyectos:

```bash
adk web
```

Para consultar los modelos disponibles en tu cuenta, ejecuta desde `model_comparison`:

```bash
python list_models.py
```

Ambos comandos requieren que las credenciales estén configuradas en el archivo `.env` local.
