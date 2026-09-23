# Travel Agent

Este proyecto muestra cómo convertir funciones normales de Python en herramientas de Google ADK y cómo coordinarlas para resolver una solicitud de varios pasos. El agente puede buscar vuelos, buscar hoteles y calcular un presupuesto total con datos simulados.

## Conceptos del ejercicio

- Crear herramientas de función personalizadas con Python.
- Usar nombres, anotaciones de tipo y docstrings para describir cada herramienta al modelo.
- Devolver diccionarios estructurados con `status` y datos de éxito o error.
- Registrar varias funciones mediante el parámetro `tools`.
- Encadenar los resultados de una herramienta como argumentos de la siguiente.
- Presentar datos estructurados al usuario en lenguaje natural.
- Normalizar nombres de ciudades para aceptar entradas en español e inglés.

## Cómo ADK convierte una función en herramienta

Cuando una función se incluye en la lista `tools`, ADK inspecciona su nombre, sus parámetros, las anotaciones de tipo, la docstring y el tipo de retorno. Con esos datos genera el esquema que recibe el modelo:

```python
def search_flights(destination: str, departure_date: str) -> dict:
    """Busca vuelos disponibles a un destino en una fecha específica."""

root_agent = Agent(
    # ...
    tools=[search_flights, search_hotels, calculate_trip_budget],
)
```

El modelo usa ese esquema para decidir qué función necesita y qué argumentos debe proporcionar. Los nombres descriptivos con el patrón verbo y sustantivo, como `search_flights` o `calculate_trip_budget`, facilitan esa selección.

El PDF recomienda parámetros obligatorios con tipos simples y serializables en JSON, por ejemplo `str`, `int`, `float`, `bool`, `list` y `dict`. Este proyecto sigue ese patrón y evita parámetros con valores predeterminados.

## Las tres herramientas

### `search_flights`

Recibe un destino y una fecha de salida. Consulta datos simulados para París y Tokio y devuelve una lista con número de vuelo, precio y duración.

### `search_hotels`

Recibe una ciudad y una fecha de entrada. Devuelve hoteles simulados con precio por noche y calificación.

### `calculate_trip_budget`

Recibe el precio del vuelo, el precio por noche y la cantidad de noches. Calcula el costo del alojamiento y lo suma al vuelo:

```text
hotel_total = hotel_price × num_nights
total = flight_price + hotel_total
```

Esta función puede usarse sola o después de las dos búsquedas. En un plan completo, el agente elige una opción de vuelo y una de hotel, toma sus precios y llama a la calculadora.

## Resultados estructurados y errores

Las herramientas devuelven diccionarios con una clave `status`. Esto ayuda al modelo a distinguir una operación correcta de un error:

```python
{
    "status": "success",
    "flights": [...],
    "count": 2,
}
```

```python
{
    "status": "error",
    "error_message": "No se encontraron vuelos a Londres...",
}
```

Ante un error, las instrucciones indican que el agente debe disculparse y sugerir los destinos disponibles. Este formato evita que tenga que interpretar excepciones técnicas y le proporciona un mensaje que puede comunicar al usuario.

Los vuelos y hoteles de este ejercicio son datos estáticos. Las fechas forman parte del resultado, pero no filtran disponibilidad real ni validan el calendario. Tampoco se realiza una reserva ni se consulta una API externa.

## Ciudades en español e inglés

El ejemplo original almacenaba las claves `paris` y `tokyo`. Al conversar en español, el modelo podía enviar `París` o `Tokio`, lo que producía un resultado de error aunque la ciudad estuviera disponible.

`normalize_city_name()` ahora:

- Elimina espacios exteriores.
- Unifica mayúsculas y minúsculas.
- Elimina acentos.
- Convierte el alias español `Tokio` en la clave interna `tokyo`.

Por eso funcionan variantes como `París`, `PARIS`, `Tokio` y `Tokyo` tanto en la búsqueda de vuelos como en la de hoteles.

## Coordinación de varias herramientas

Para una solicitud completa, el flujo esperado es:

```text
Solicitud del usuario
        │
        ├─ search_flights(destino, fecha)
        ├─ search_hotels(ciudad, fecha)
        └─ calculate_trip_budget(precio_vuelo, precio_hotel, noches)
                         │
                         ▼
             Plan y desglose del costo
```

El agente decide el orden mediante sus instrucciones y las descripciones de las funciones. ADK gestiona las llamadas, mientras cada herramienta realiza una tarea pequeña y predecible.

## Pruebas sugeridas

| Solicitud | Comportamiento esperado |
| --- | --- |
| «Quiero volar a París el 15-12-2026» | Llama a `search_flights` y presenta dos opciones. |
| «Planifica un viaje de 3 noches a Tokio desde el 20-12-2026» | Busca vuelos y hoteles, elige opciones y calcula el presupuesto. |
| «Busca hoteles en Londres para el 10-11-2026» | Devuelve el error estructurado y sugiere París o Tokio. |
| «¿Cuánto cuesta un vuelo de $450 y un hotel de $150 durante 4 noches?» | Usa únicamente `calculate_trip_budget` y devuelve un total de $1,050. |

En la interfaz de ADK puedes revisar los eventos para confirmar qué funciones se llamaron y qué argumentos generó el modelo. La redacción de la respuesta final puede variar.

## Diferencia con otros tipos de herramientas

Las funciones personalizadas son adecuadas para lógica propia del dominio, reglas de precios, sistemas internos o integraciones que controla la aplicación. A diferencia de las herramientas integradas de [`research_assistant`](../research_assistant/) y [`math_assistant`](../math_assistant/), aquí el desarrollador implementa y mantiene la lógica. A diferencia de [`file_reader_assistant`](../file_reader_assistant/), las herramientas se ejecutan directamente como funciones del proyecto y no mediante un servidor MCP.

## Archivos y ejecución

- `agent.py`: contiene la normalización, las tres herramientas y `root_agent`.
- `__init__.py`: permite que ADK cargue el paquete.

Configura `GOOGLE_API_KEY` en el archivo `.env` local y ejecuta desde `adk-workspace`:

```bash
adk web
```

Selecciona `travel_agent` y prueba las solicitudes anteriores.
