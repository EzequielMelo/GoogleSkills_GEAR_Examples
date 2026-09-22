# Geography Assistant

Este ejercicio introduce las herramientas de función en Google Agent Development Kit (ADK). El agente responde preguntas sobre capitales usando `get_capital_city`, una función de Python que consulta un diccionario local de países y capitales.

## Qué se practica

- Definir una herramienta con una función de Python y ofrecerla al agente mediante `tools=[get_capital_city]`.
- Describir su propósito y su parámetro con un nombre claro, una docstring y anotaciones de tipo.
- Dejar que el agente extraiga el país de la pregunta, llame a la función y transforme el resultado en una respuesta natural.
- Manejar consultas con varios países y países ausentes del diccionario.
- Normalizar nombres de países en español e inglés para que entradas como `Japón` y `Japan` encuentren la misma capital.

## Cómo funciona la herramienta

La parte central de `agent.py` es una función con una tarea concreta:

```python
def get_capital_city(country: str) -> str:
    """Recupera la ciudad capital de un país específico."""
    # Consulta el diccionario local y devuelve la capital o un mensaje de error.
```

Al incluir la función en `tools`, ADK la presenta al modelo como una herramienta. Su nombre, docstring y parámetro `country: str` le indican para qué sirve y qué argumento debe proporcionar. La instrucción del agente le pide usarla antes de responder preguntas sobre capitales:

```python
tools=[get_capital_city]
```

La función ejecuta lógica definida en Python; el modelo decide cuándo llamarla y redacta la respuesta a partir del resultado. Para una pregunta como «¿Cuál es la capital de Japón?», el flujo esperado es:

```text
Pregunta → llamada a get_capital_city(country="Japón")
         → resultado "Tokyo"
         → respuesta del agente: «La capital de Japón es Tokio»
```

El argumento podría llegar como `Japón` o `Japan`. `normalize_country_name()` elimina espacios exteriores, unifica mayúsculas y minúsculas y quita acentos; el diccionario incluye algunas variantes en español e inglés. Esta adaptación resuelve el caso en que el agente enviaba `Japón` pero el diccionario original solo tenía `japan`.

## Qué aporta una herramienta

Según el material del curso, las herramientas amplían lo que puede hacer un agente: consultar datos, realizar cálculos o interactuar con otros sistemas. ADK admite funciones propias, herramientas integradas y, en flujos más avanzados, agentes usados como herramientas. Este proyecto utiliza únicamente una función propia.

El ciclo general tiene cinco momentos: el modelo interpreta la solicitud, selecciona la herramienta, proporciona sus argumentos, recibe el resultado y redacta la respuesta. No toda pregunta necesita una llamada: una solicitud general como «Cuéntame sobre geografía» puede responderse directamente. En cambio, la instrucción de este ejercicio exige consultar la función cuando se pregunta por una capital.

La fuente de datos aquí es un **diccionario local y limitado**. No se consulta una API ni una base de datos externa, y solo se pueden confirmar las capitales incluidas en `agent.py`. Para un país ausente, la función devuelve un mensaje indicando que no tiene esa información; el agente debe comunicar esa limitación aunque conozca la respuesta por otros medios.

## Pruebas sugeridas

Ejecuta `adk web` desde la carpeta `adk-workspace`, selecciona `geography_assistant` y prueba estas preguntas:

| Pregunta | Qué observar |
| --- | --- |
| «¿Cuál es la capital de Japón?» | Llamada a la herramienta con `Japón` o `Japan`; resultado `Tokyo`. |
| «Dime las capitales de Francia, Alemania y Brasil» | Una consulta por país y una respuesta que reúne los tres resultados. |
| «¿Cuál es la capital de Islandia?» | Mensaje de ausencia de datos; Islandia no está en el diccionario. |
| «Cuéntame sobre geografía» | Respuesta general sin necesidad de consultar capitales. |

Las respuestas finales pueden variar en redacción e idioma. En la vista de eventos de ADK puedes comprobar si hubo una llamada a `get_capital_city` y qué argumento recibió; la respuesta por sí sola no demuestra que el agente haya usado la herramienta.

## Archivos

- `agent.py`: contiene la normalización de nombres, la función `get_capital_city` y `root_agent`.
- `__init__.py`: permite que ADK cargue el paquete del agente.

El archivo `.env` local guarda la configuración de acceso a Gemini y está excluido del repositorio mediante `.gitignore`.
