# Namespace Demo

Este proyecto demuestra cómo los prefijos de las claves de estado determinan su alcance y persistencia en Google Agent Development Kit (ADK). El ejercicio compara datos temporales, datos de una conversación, preferencias de un usuario y configuración compartida por toda la aplicación.

## Conceptos practicados

- Los cuatro alcances del estado: `temp:`, sesión, `user:` y `app:`.
- Inicialización del estado mediante `create_session(state=...)`.
- Lectura del estado actual con `ReadonlyContext`.
- Creación de estado temporal mediante `before_agent_callback`.
- Persistencia entre turnos y entre sesiones.
- Actualización de una copia de sesión mediante `get_session()`.
- Almacenamiento de la respuesta del agente con `output_key`.

## Los cuatro namespaces

| Namespace | Ejemplo | Alcance | Duración |
| --- | --- | --- | --- |
| Temporal | `temp:step` | Invocación actual | Se descarta al terminar el turno |
| Sesión | `topic` | Conversación actual | Permanece durante esa sesión |
| Usuario | `user:theme` | Mismo usuario dentro de una app | Se comparte entre sus sesiones |
| Aplicación | `app:version` | Todos los usuarios de la app | Se comparte globalmente en la app |

Una **invocación** abarca el proceso completo desde que llega un mensaje hasta que el agente produce su respuesta. Una **sesión** puede contener varias invocaciones o turnos de una misma conversación.

## Estado temporal: `temp:`

El estado temporal sirve para datos que solamente deben existir durante la invocación actual, por ejemplo:

- Pasos intermedios de procesamiento.
- Resultados de validación usados dentro del mismo turno.
- Marcas compartidas entre herramientas durante una invocación.
- Datos que no deben guardarse en la sesión.

En este proyecto, `temp:step` se establece antes de ejecutar el agente:

```python
def set_temporary_state(callback_context: CallbackContext) -> None:
    callback_context.state["temp:step"] = "initialization"
```

El callback se ejecuta en cada invocación. Por eso el agente puede leer `temp:step` mientras procesa cada turno, pero `get_session()` demuestra que el valor no se almacenó una vez finalizado el turno.

No debe usarse `temp:` para datos necesarios en mensajes posteriores.

## Estado de sesión: sin prefijo

Una clave sin prefijo pertenece a la conversación actual:

```python
"topic": "state management"
```

`topic` continúa disponible en el segundo turno de `session1`, pero no aparece al crear `session2`. Este alcance es apropiado para:

- El tema actual de la conversación.
- El progreso de una tarea.
- Contadores de turnos.
- Datos de un carrito temporal.
- Indicadores como `needs_clarification`.

## Estado de usuario: `user:`

Las claves `user:` están vinculadas a la combinación de `app_name` y `user_id`:

```python
"user:theme": "dark"
```

Cuando el ejercicio crea `session2` para el mismo usuario y la misma aplicación, ADK incorpora nuevamente `user:theme`. Algunos usos habituales son:

- Idioma preferido.
- Tema visual.
- Nivel de suscripción.
- Preferencias y datos de perfil.

No conviene utilizar este namespace para información que solo tiene sentido dentro de una conversación concreta.

## Estado de aplicación: `app:`

Las claves `app:` se comparten entre los usuarios y sesiones asociados al mismo `app_name`:

```python
"app:name": "Demostración de espacios de nombres"
"app:version": "2.0"
```

Son adecuadas para:

- Versión de la aplicación.
- Endpoints compartidos.
- Feature flags.
- Configuración global.
- Plantillas comunes.

No deben contener preferencias personales ni información específica de una sesión.

## Inicialización correcta del estado

El estado persistente se entrega al crear la primera sesión:

```python
session = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="session1",
        state={
            "app:name": "Demostración de espacios de nombres",
            "app:version": "2.0",
            "user:theme": "dark",
            "topic": "state management",
        },
    )
)
```

La versión actual de ADK devuelve una copia de la sesión. Modificar directamente esa copia con `session.state[...] = ...` no garantiza que el servicio almacene los cambios. Por eso el ejemplo proporciona el estado inicial mediante `create_session()` y vuelve a consultarlo con `get_session()` después de cada turno.

Tanto `create_session()` como `get_session()` son asíncronos en esta versión, por lo que el script los ejecuta con `asyncio.run()`.

## Instrucciones basadas en el estado

El agente utiliza una función que recibe `ReadonlyContext`:

```python
def build_instruction(context: ReadonlyContext) -> str:
    app_version = context.state.get("app:version", "1.0")
    user_theme = context.state.get("user:theme", "not set")
    topic = context.state.get("topic", "not set")
    current_step = context.state.get("temp:step", "not set")
```

Este patrón permite leer cualquier namespace y proporcionar valores predeterminados. Se utiliza porque la versión instalada reconoce `{key}` y `{key?}`, pero no interpreta la forma `{key?valor predeterminado}` descrita en el material original del curso.

Las instrucciones son dinámicas: ADK llama a `build_instruction()` durante cada ejecución y el agente recibe los valores visibles en esa invocación.

## `output_key`

El agente contiene:

```python
output_key="response"
```

Como la clave no tiene prefijo, la respuesta final se guarda en el estado de `session1`. No se transfiere a `session2`. Si fuera `user:response`, se compartiría entre sesiones del usuario; con `temp:response`, solo existiría durante la invocación.

## Flujo que comprueba el ejercicio

```text
session1, turno 1
  temp:step     → visible durante el turno, luego descartado
  topic         → almacenado en session1
  user:theme    → almacenado para user1
  app:version   → almacenado para namespace_demo

session1, turno 2
  topic         → continúa disponible
  temp:step     → se crea nuevamente y vuelve a descartarse

session2, mismo usuario y app
  topic         → no existe
  user:theme    → se hereda
  app:version   → se hereda
```

## Cómo elegir un namespace

Utiliza el alcance más limitado que satisfaga la necesidad:

1. ¿El dato solo se necesita durante el turno actual? Usa `temp:`.
2. ¿Debe permanecer durante esta conversación? Usa una clave sin prefijo.
3. ¿Debe estar disponible en futuras sesiones del mismo usuario? Usa `user:`.
4. ¿Debe compartirse con todos los usuarios de la aplicación? Usa `app:`.

Conservar datos en un alcance mayor al necesario puede producir información obsoleta, cruces entre conversaciones o exposición accidental de datos.

## Persistencia de `InMemorySessionService`

El servicio usado en este ejercicio conserva los valores de sesión, usuario y aplicación solamente mientras el proceso de Python permanece activo. Al reiniciar el programa se pierde toda la información.

Para persistencia real entre reinicios se necesita un servicio respaldado por almacenamiento, como una implementación de base de datos compatible con ADK. Los prefijos definen el alcance lógico, pero la duración física también depende del `SessionService` elegido.

## Archivos

- `agent.py`: define el agente, las instrucciones dinámicas y el callback temporal.
- `test_namespaces.py`: ejecuta dos turnos y crea una segunda sesión para comparar la persistencia.
- `__init__.py`: expone el agente como paquete de Python.

## Ejecutar el ejercicio

Configura `GOOGLE_API_KEY` en `.env` y ejecuta desde esta carpeta:

```bash
python test_namespaces.py
```

También puedes abrir el agente desde la carpeta general:

```bash
adk web
```
