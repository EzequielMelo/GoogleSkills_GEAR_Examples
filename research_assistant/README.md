# Research Assistant

Este proyecto usa la herramienta integrada `google_search` de Google ADK para investigar preguntas que requieren información reciente. El agente busca en la web, elabora una respuesta basada en los resultados y solicita citar las fuentes utilizadas.

## Conceptos del ejercicio

- Incorporar una herramienta ya implementada por ADK mediante `tools=[google_search]`.
- Distinguir una pregunta que necesita datos actuales de otra que puede responderse sin búsqueda.
- Fundamentar la respuesta en los resultados obtenidos y permitir que el lector compruebe las fuentes.
- Reconocer cuando la búsqueda no aporta información suficiente.

## Configuración del agente

La herramienta se importa y se entrega al agente así:

```python
from google.adk.tools import google_search

root_agent = Agent(
    model="gemini-3.5-flash",
    name="research_assistant",
    tools=[google_search],
    # ...
)
```

El PDF del curso usa `gemini-2.5-flash`; el código de este proyecto usa `gemini-3.5-flash`. La herramienta de búsqueda está disponible para el agente mediante la lista `tools`. No hace falta escribir una función de búsqueda propia.

Cuando la pregunta requiere información reciente, el flujo esperado es:

```text
Pregunta → búsqueda web → resultados y fuentes → síntesis del agente
```

Las instrucciones de `agent.py` indican que el agente debe basarse en los resultados, citar las fuentes y reconocer los vacíos de información. La fundamentación ayuda a verificar una respuesta, pero no sustituye la lectura crítica de las fuentes.

## Pruebas sugeridas

| Pregunta | Qué observar |
| --- | --- |
| «¿Cuáles son los avances recientes en energía renovable?» | Búsqueda de información actual y referencias a fuentes. |
| «¿Quién dirige actualmente una empresa que conozcas?» | Verificación de un dato que puede cambiar con el tiempo. |
| «Compara vehículos eléctricos y de hidrógeno» | Síntesis de varias perspectivas con fuentes. |

En la interfaz de ADK, revisa los eventos de la ejecución para comprobar si el agente utilizó la búsqueda. Una respuesta con apariencia de cita no prueba por sí sola que se haya hecho una consulta web.

## Diferencia con una herramienta propia

En [`geography_assistant`](../geography_assistant/) escribimos una función de Python para consultar un diccionario local. Aquí importamos una capacidad integrada para consultar información externa. El PDF también presenta otras herramientas integradas, como la ejecución de código; esa segunda capacidad se practica por separado en [`math_assistant`](../math_assistant/).

Si desarrollas una interfaz propia para mostrar resultados fundamentados, revisa los requisitos de presentación de las sugerencias de búsqueda que describe el PDF. La visualización de esa información corresponde a la interfaz, no a la configuración de `agent.py`.

## Archivos y ejecución

- `agent.py`: define el agente y habilita `google_search`.
- `__init__.py`: permite a ADK cargar el paquete.

Configura tu clave de Gemini en el `.env` local y ejecuta desde la carpeta general `adk-workspace`:

```bash
adk web
```

Selecciona `research_assistant`. La búsqueda necesita acceso a la API y está sujeta a las cuotas del proyecto; si aparece `429 RESOURCE_EXHAUSTED`, consulta el uso y los límites antes de repetir la solicitud.
