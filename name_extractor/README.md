# Name Extractor

Este proyecto introduce el estado de sesión en Google ADK. El agente extrae el nombre de una persona y `output_key` hace que la respuesta quede guardada para poder consultarla durante la misma sesión.

## Conceptos practicados

- Extracción de un dato específico desde lenguaje natural.
- Uso de `output_key="user_name"` para guardar la salida del agente.
- Creación de sesiones en memoria con `InMemorySessionService`.
- Ejecución programática mediante `Runner`.
- Lectura del estado con `session.state`.
- Comprobación de la persistencia entre turnos de una misma sesión.

## Cómo funciona `output_key`

Cuando el agente produce su respuesta final, ADK la asigna automáticamente a la clave configurada:

```python
output_key="user_name"
```

El valor puede recuperarse después mediante:

```python
session.state.get("user_name")
```

El estado pertenece a una sesión identificada por la combinación de aplicación, usuario y sesión. En este ejercicio se utiliza un servicio en memoria, por lo que los datos sobreviven entre turnos mientras el proceso continúa, pero no se conservan al reiniciarlo.

## Archivos

- `agent.py`: define el agente y su `output_key`.
- `test_state.py`: crea una sesión, ejecuta dos turnos e inspecciona el estado.
- `__init__.py`: expone el módulo como paquete de Python.

## Ejecutar la prueba

Configura primero tu archivo `.env` y, desde la carpeta `name_extractor`, ejecuta:

```bash
python test_state.py
```

La salida muestra la respuesta del agente, el contenido de `session.state` y una comprobación de que `user_name` sigue disponible en el segundo turno.
