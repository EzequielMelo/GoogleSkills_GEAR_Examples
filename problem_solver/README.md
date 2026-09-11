# Problem Solver

Este proyecto presenta la planificación en Google Agent Development Kit (ADK). El agente utiliza `BuiltInPlanner` para abordar problemas complejos de forma sistemática: entender el problema, analizar alternativas, preparar un plan y producir recomendaciones prácticas.

## Conceptos practicados

- Incorporación de un planificador mediante el parámetro singular `planner`.
- Uso de `BuiltInPlanner` con las capacidades de pensamiento de Gemini.
- Configuración de `ThinkingConfig`.
- Asignación de un presupuesto de pensamiento con `thinking_budget`.
- Inclusión de pensamientos o resúmenes de razonamiento mediante `include_thoughts` cuando el modelo lo admite.
- Adaptación del esfuerzo de razonamiento a la complejidad de la consulta.

## Configuración del agente

El planificador se importa desde ADK y su configuración desde el SDK de Google Gen AI:

```python
from google.adk.planners import BuiltInPlanner
from google.genai import types
```

Después se conecta al agente mediante `planner`:

```python
planner=BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_budget=2048,
    )
)
```

Es importante utilizar `planner` en singular. Este parámetro habilita la estrategia de planificación para el agente.

## `ThinkingConfig`

`ThinkingConfig` controla cómo el modelo emplea sus capacidades de pensamiento:

- `thinking_budget=2048`: reserva hasta 2048 tokens para el proceso de pensamiento, separados de los tokens de la respuesta final. Un presupuesto mayor puede ayudar en tareas complejas, pero también puede aumentar la latencia y el consumo.
- `include_thoughts=True`: solicita que la respuesta incluya la información de pensamiento que el modelo y la API permitan exponer. Es útil durante el aprendizaje y la depuración; en una aplicación de producción normalmente se evalúa si conviene mostrarla al usuario.

El presupuesto no obliga al modelo a utilizar siempre todos los tokens. La compatibilidad y el comportamiento exacto de estas opciones pueden variar según el modelo seleccionado.

## Elección del planificador

### `BuiltInPlanner`

Es la opción adecuada cuando el modelo de Gemini utilizado posee capacidades de pensamiento integradas, como los modelos compatibles de las familias Gemini 2.0 y 2.5. Sus ventajas principales son:

- Aprovecha el razonamiento nativo del modelo.
- Produce un proceso de resolución más natural.
- Permite configurar la profundidad con `thinking_budget`.
- Puede solicitar información de pensamiento con `include_thoughts`.

Este curso se concentra en `BuiltInPlanner` porque los ejercicios utilizan modelos de Gemini.

### `PlanReActPlanner`

Puede ser más apropiado cuando:

- Se trabaja con un modelo sin capacidades de pensamiento integradas.
- Se necesita una estructura explícita y estricta, como `PLANIFICACIÓN`, `ACCIÓN`, `RAZONAMIENTO` y `RESPUESTA_FINAL`.
- El agente utiliza muchas herramientas y resulta útil separar claramente las fases de planificación y acción.
- Se construyen flujos avanzados o sistemas de múltiples agentes.

La elección depende tanto del modelo como de la tarea. No existe un planificador universalmente óptimo para todos los agentes.

## Cuándo utilizar planificación

La planificación suele aportar valor en tareas como:

- Resolución de problemas de varios pasos.
- Comparación de alternativas y análisis de compensaciones.
- Toma de decisiones complejas.
- Identificación de riesgos, consecuencias y casos extremos.
- Depuración del comportamiento del agente.
- Elaboración de estrategias con acciones dependientes entre sí.

Generalmente puede omitirse para:

- Preguntas sencillas y directas.
- Búsquedas fácticas rápidas.
- Tareas de un solo paso.
- Respuestas urgentes en las que importa minimizar la latencia.

## ¿Qué ocurre con las preguntas sencillas?

Tener un planificador habilitado no significa necesariamente que todas las respuestas serán largas o complejas. Ante una consulta directa, el modelo puede responder de manera breve y utilizar muy poco esfuerzo adicional. El agente adapta la profundidad del proceso a la dificultad percibida de la tarea.

Aun así, si una aplicación solo recibe solicitudes simples, omitir la planificación puede reducir configuración, latencia y consumo innecesarios.

## Estrategia del agente

Las instrucciones de `strategic_problem_solver` organizan su trabajo en cuatro etapas:

1. **Entender:** dividir el problema en componentes.
2. **Analizar:** estudiar enfoques posibles y sus compensaciones.
3. **Planificar:** construir una estrategia paso a paso.
4. **Ejecutar:** entregar recomendaciones claras y aplicables.

Además, le solicitan considerar riesgos, mitigaciones, casos extremos y consecuencias a corto y largo plazo. Las instrucciones definen el método de trabajo, mientras que `BuiltInPlanner` proporciona el soporte de razonamiento del modelo.

## Archivos

- `agent.py`: define el agente y configura `BuiltInPlanner`.
- `__init__.py`: importa el módulo para que ADK reconozca el proyecto como paquete de Python.

## Ejecutar el agente

Desde la carpeta que contiene todos los proyectos:

```bash
adk web
```

Selecciona `problem_solver` y prueba primero una consulta sencilla. Después compárala con un problema que requiera varias decisiones, restricciones o análisis de riesgos para observar cómo cambia la profundidad de la respuesta.
