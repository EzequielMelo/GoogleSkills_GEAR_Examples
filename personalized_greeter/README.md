# Personalized Greeter

Este proyecto muestra cómo personalizar las instrucciones de un agente con datos almacenados en el estado de sesión. El agente adapta el saludo, el idioma y la información de membresía según los datos disponibles para cada usuario.

## Conceptos practicados

- Lectura de datos desde `session.state`.
- Instrucciones dinámicas basadas en el contexto de ejecución.
- Uso de `ReadonlyContext` para consultar el estado sin modificarlo.
- Valores predeterminados cuando una clave no existe.
- Creación asíncrona de sesiones con `InMemorySessionService`.
- Pruebas de sesiones sin estado, con estado parcial y con estado completo.
- Ejecución programática del agente mediante `Runner`.

## Plantillas de estado de ADK

ADK puede insertar valores del estado directamente en una cadena de instrucciones. Por ejemplo:

```python
instruction="Hola, {user_name}. Responde en {user_language}."
```

Si el estado contiene:

```python
{
    "user_name": "Álex",
    "user_language": "Spanish",
}
```

antes de llamar al modelo, ADK transforma la instrucción en algo equivalente a:

```text
Hola, Álex. Responde en Spanish.
```

La sustitución ocurre antes de cada invocación, por lo que utiliza los valores actuales de la sesión. Las claves distinguen mayúsculas de minúsculas: `{name}` y `{Name}` son variables diferentes.

## Variables obligatorias y opcionales

La versión de ADK utilizada por este proyecto admite estas formas nativas:

- `{key}`: inserta el valor y produce un `KeyError` si la clave no existe.
- `{key?}`: inserta el valor si existe o una cadena vacía si no existe.

Ejemplo opcional:

```python
instruction="Hola, {user_name?}"
```

El material original del ejercicio también presenta expresiones como `{user_name?usuario}` y bloques condicionales dentro de llaves. Esa sintaxis ampliada no es interpretada como valor predeterminado por la versión instalada de ADK. Por eso la implementación final utiliza una función de instrucciones.

## Instrucciones dinámicas con `ReadonlyContext`

El agente recibe `build_instruction` en lugar de una cadena fija:

```python
def build_instruction(context: ReadonlyContext) -> str:
    user_name = context.state.get("user_name", "usuario")
    user_language = context.state.get("user_language", "English")
    membership_tier = context.state.get("membership_tier", "free")

    return f"""
    Nombre: {user_name}
    Idioma preferido: {user_language}
    Membresía: {membership_tier}
    """
```

`context.state` ofrece una vista de solo lectura del estado de la sesión actual. El método `get()` permite proporcionar valores predeterminados sin generar errores:

- `usuario` cuando no existe `user_name`.
- `English` cuando no existe `user_language`.
- `free` cuando no existe `membership_tier`.

ADK invoca esta función para construir las instrucciones correspondientes a la sesión antes de enviar la solicitud al modelo.

## Flujo del ejercicio

```text
Estado de sesión
        │
        ▼
build_instruction(context)
        │ aplica valores actuales o predeterminados
        ▼
Instrucción personalizada
        │
        ▼
Modelo Gemini → saludo adaptado
```

El archivo de prueba crea tres sesiones independientes:

1. `session1` no recibe estado y utiliza todos los valores predeterminados.
2. `session2` solamente recibe `user_name="Álex"`.
3. `session3` recibe nombre, idioma y nivel de membresía.

Las sesiones son independientes para que cada caso sea reproducible y no dependa de los cambios realizados en una prueba anterior.

## Creación asíncrona de sesiones

En la versión actual de ADK, `create_session()` es un método asíncrono. El script lo ejecuta de esta manera:

```python
session = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="session3",
        state={"user_name": "Álex"},
    )
)
```

Si se llama sin `await` o `asyncio.run()`, la sesión no llega a crearse y `Runner` produce un `SessionNotFoundError`.

## Archivos

- `agent.py`: define el agente y la función que genera sus instrucciones dinámicas.
- `test_templating.py`: carga las variables de entorno, crea tres sesiones y compara las respuestas.
- `__init__.py`: expone el módulo como paquete de Python.

## Ejecutar la prueba

Configura `GOOGLE_API_KEY` en el archivo `.env` local. Después, desde `personalized_greeter`, ejecuta:

```bash
python test_templating.py
```

El script imprimirá un saludo para cada configuración de estado y finalmente mostrará el estado completo de la tercera sesión.

También puedes abrir el agente desde la carpeta general del repositorio:

```bash
adk web
```

## Cuándo utilizar este patrón

Las instrucciones basadas en estado son útiles para:

- Personalizar idioma, tono o preferencias.
- Proporcionar al agente información obtenida en turnos anteriores.
- Insertar datos exactos procedentes de una aplicación.
- Cambiar el comportamiento sin crear un agente distinto para cada usuario.
- Compartir contexto entre pasos de un flujo de agentes.

Para aplicaciones persistentes, `InMemorySessionService` debe sustituirse por un servicio de sesión adecuado, ya que su contenido desaparece al finalizar el proceso.
