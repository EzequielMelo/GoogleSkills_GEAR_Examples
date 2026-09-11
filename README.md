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

Cada proyecto contiene su propio `README.md` con una explicación del código y formas de probarlo.

## Configuración general

Los ejercicios requieren Python, Google ADK y una clave para acceder al modelo de Gemini. Las credenciales deben guardarse en archivos `.env` locales. Estos archivos están excluidos de Git para evitar publicar secretos accidentalmente.

Ejemplo orientativo:

```env
GOOGLE_API_KEY=tu_clave
```

No incluyas claves reales en commits ni en archivos de ejemplo.
