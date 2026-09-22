# Math Assistant

Este proyecto incorpora la ejecución de código integrada de Google ADK para resolver cálculos matemáticos. En lugar de depender únicamente de la respuesta generada por el modelo, el agente puede ejecutar código para obtener y comprobar resultados numéricos.

## Conceptos del ejercicio

- Activar la ejecución de código con `code_executor=BuiltInCodeExecutor()`.
- Utilizar código para operaciones numéricas, estadísticas y análisis de datos.
- Explicar los pasos del cálculo y contrastar el resultado con la ejecución.
- Distinguir el parámetro `code_executor` de la lista `tools` utilizada por otros agentes.

## Configuración del agente

```python
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    model="gemini-3.5-flash",
    name="root_agent",
    code_executor=BuiltInCodeExecutor(),
    # ...
)
```

El PDF del curso usa `gemini-2.5-flash` y llama al agente `math_assistant`. Este proyecto utiliza `gemini-3.5-flash` y `name="root_agent"`; la carpeta del proyecto sigue llamándose `math_assistant`, que es el nombre que debes seleccionar en `adk web`.

Aquí la ejecución se configura mediante `code_executor`, no con `tools=[...]`. Las instrucciones piden al agente usar código para los cálculos numéricos, explicar el procedimiento y verificar la respuesta.

El flujo esperado es:

```text
Problema → código de cálculo → ejecución → resultado → explicación
```

Ejecutar código reduce errores aritméticos del modelo, pero sigue siendo necesario revisar que la fórmula, los datos de entrada, las unidades y el redondeo sean correctos.

## Pruebas sugeridas

| Pregunta | Qué observar |
| --- | --- |
| «Calcula una propina del 15 % sobre $87.50» | Operación `87.50 × 0.15 = 13.125`; con redondeo monetario habitual, $13.13. |
| «Calcula el monto de $5,000 al 6 % anual durante 8 años, con capitalización mensual» | Uso de `5000 × (1 + 0.06/12) ** (12 × 8)` y explicación del interés. |
| «Calcula media, mediana y desviación estándar de 12, 15, 18, 20, 22, 25, 28 y 30» | Ejecución de código y aclaración de si la desviación estándar es poblacional o muestral. |

En la interfaz de ADK puedes inspeccionar los eventos para ver si se ejecutó código. La redacción exacta puede variar entre ejecuciones.

## Relación con los otros ejercicios

[`research_assistant`](../research_assistant/) usa una herramienta integrada para obtener información web. Este agente utiliza otra capacidad integrada para calcular. Ambos ejemplos se mantienen separados en el curso para mostrar cada configuración con claridad. A diferencia de [`geography_assistant`](../geography_assistant/), aquí no escribimos la implementación de la herramienta en Python.

## Archivos y ejecución

- `agent.py`: define el agente y configura `BuiltInCodeExecutor`.
- `__init__.py`: permite a ADK cargar el paquete.

Configura tu clave de Gemini en el `.env` local y ejecuta desde `adk-workspace`:

```bash
adk web
```

Selecciona `math_assistant` y prueba los ejemplos anteriores. La ejecución del modelo requiere acceso a la API y está sujeta a las cuotas del proyecto.
