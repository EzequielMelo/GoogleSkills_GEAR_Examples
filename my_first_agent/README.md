# My First Agent

Este proyecto presenta la estructura mínima de un agente creado con Google Agent Development Kit (ADK). El agente funciona como tutor de álgebra y está configurado para explicar los problemas de forma gradual, con un tono paciente y motivador.

## Conceptos practicados

- Creación de un agente mediante la clase `Agent`.
- Elección del modelo con el parámetro `model`.
- Uso de `name` y `description` para identificar el agente.
- Definición de su comportamiento mediante una instrucción multilínea.
- Exposición de `root_agent`, el punto de entrada que ADK espera encontrar.

## Archivos

- `agent.py`: define y configura el agente tutor.
- `__init__.py`: importa el módulo del agente para que el proyecto sea reconocido como paquete de Python.

## Ejecutar el agente

Desde la carpeta que contiene todos los proyectos:

```bash
adk web
```

Después, selecciona `my_first_agent` en la interfaz de ADK y conversa con el tutor usando un problema de álgebra.

## Qué observar

La propiedad `instruction` actúa como la guía principal del agente. En este ejercicio determina tanto su rol como su método de enseñanza: dividir problemas, orientar sin revelar inmediatamente la solución y reforzar el progreso del estudiante.
