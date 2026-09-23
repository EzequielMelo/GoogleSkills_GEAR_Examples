# Customer Support

Este proyecto crea un agente de atención al cliente para una tienda en línea. El ejercicio se centra en escribir instrucciones estratégicas que permitan al modelo seleccionar, ordenar y combinar herramientas de forma confiable, además de responder correctamente ante errores y derivar los casos que requieren intervención humana.

Los pedidos y las operaciones son simulados: no se consulta una tienda real, no se mueve dinero y no se contacta realmente a un supervisor.

## Conceptos del ejercicio

- Diseñar herramientas pequeñas y con una única responsabilidad.
- Indicar explícitamente cuándo debe usarse cada herramienta.
- Coordinar varias llamadas en un orden definido.
- Devolver resultados y errores mediante diccionarios estructurados.
- Adaptar la respuesta según cada `error_type`.
- Definir criterios claros para derivar un caso a una persona.
- Separar la lógica determinística de Python de las decisiones conversacionales del agente.

## Herramientas disponibles

### `check_order_status`

Valida el formato del ID y busca el pedido en `ORDERS_DB`. Cuando lo encuentra, devuelve su estado, total y cliente. Puede producir dos errores:

- `invalid_format`: el ID no comienza con `ORD`.
- `not_found`: el formato es válido, pero el pedido no existe.

### `process_refund`

Procesa un reembolso únicamente para pedidos con estado `delivered`. Recibe el ID y el motivo expresado por el cliente. En caso de éxito devuelve el importe, una referencia y un plazo estimado de cinco días.

Sus errores posibles son:

- `order_not_found`: el pedido no existe.
- `cannot_refund`: el pedido todavía no fue entregado.

### `escalate_to_supervisor`

Simula la derivación de un problema complejo y devuelve un ID de ticket y un plazo estimado de respuesta. Se utiliza cuando las herramientas disponibles no resuelven el caso, se solicita una excepción o el cliente pide hablar con un supervisor.

## Instrucciones estratégicas

Una docstring explica al modelo qué hace una función, qué argumentos recibe y qué devuelve. Las instrucciones del agente cumplen otra función: describen **cuándo** utilizarla, qué hacer con su resultado y cómo coordinarla con las demás.

El PDF organiza estas instrucciones en cuatro áreas:

1. **Selección de herramientas:** relacionar cada intención del usuario con la función apropiada.
2. **Flujos de trabajo:** especificar el orden de las operaciones cuando una acción depende de otra.
3. **Manejo de errores:** indicar una respuesta distinta para cada tipo de fallo.
4. **Derivación:** establecer cuándo y cómo transferir un problema que el agente no puede resolver.

En `agent.py`, los nombres de las funciones aparecen directamente en las instrucciones. Esto reduce la ambigüedad al elegir una herramienta y permite describir reglas como «primero verifica el pedido y luego procesa el reembolso».

## Flujo de una consulta

Una consulta de estado requiere una sola herramienta:

```text
ID proporcionado
      │
      ▼
check_order_status
      │
      ├─ success ───────► informar estado y detalles
      ├─ not_found ─────► pedir que se revise el ID
      └─ invalid_format ► explicar el formato ORD123
```

El reembolso es un flujo secuencial. Verificar antes de actuar evita intentar una operación sobre un pedido inexistente:

```text
Solicitud de reembolso
          │
          ▼
check_order_status
          │
          ├─ error ─► orientar al cliente y detener el flujo
          │
          ▼
process_refund
          │
          ├─ success ───────► confirmar importe, referencia y plazo
          └─ cannot_refund ─► explicar la política y ofrecer derivación
```

## Resultados y errores estructurados

Todas las herramientas devuelven diccionarios con una clave `status`. Los errores incluyen además un tipo estable y un mensaje legible:

```python
{
    "status": "error",
    "error_type": "invalid_format",
    "error_message": "Los IDs de pedido deben comenzar con 'ORD'...",
}
```

Este contrato permite que el agente tome decisiones a partir de datos concretos, sin interpretar excepciones ni inventar resultados. El PDF destaca que no todos los errores se tratan igual: una entrada inválida requiere enseñar el formato, un pedido inexistente requiere verificar el dato y una restricción de reembolso puede requerir una derivación.

## Datos de prueba

| Pedido | Estado | Total | Resultado de un reembolso |
| --- | --- | ---: | --- |
| `ORD123` | `shipped` | USD 99.99 | No permitido |
| `ORD456` | `processing` | USD 149.99 | No permitido |
| `ORD789` | `delivered` | USD 249.99 | Permitido |

Los IDs son sensibles a mayúsculas y minúsculas: el ejemplo espera `ORD123`, no `ord123`.

## Pruebas sugeridas

| Solicitud | Comportamiento esperado |
| --- | --- |
| «¿Dónde está mi pedido ORD123?» | Llama a `check_order_status` y comunica que fue enviado. |
| «Verifica el pedido 123» | Recibe `invalid_format`, explica el prefijo `ORD` y pide el ID correcto. |
| «¿Cuál es el estado de ORD999?» | Recibe `not_found` y solicita comprobar el ID. |
| «Quiero devolver ORD789 porque no era lo que esperaba» | Verifica el pedido, procesa el reembolso y confirma importe, referencia y plazo. |
| «Quiero el reembolso de ORD456» | Verifica, recibe `cannot_refund`, explica la regla y ofrece una derivación. |
| «Quiero hablar con un supervisor por ORD123» | Llama a `escalate_to_supervisor` y comunica el ticket y el plazo estimado. |

En la interfaz de ADK pueden revisarse los eventos para confirmar el orden de las llamadas, los argumentos generados y los resultados devueltos por cada herramienta.

## Buenas prácticas resumidas del PDF

- Usar nombres descriptivos con el patrón verbo-sustantivo.
- Añadir anotaciones de tipo y docstrings completas.
- Mantener cada función enfocada en una sola operación.
- Conservar un formato de retorno coherente entre herramientas.
- Documentar tanto los caminos exitosos como todos los errores previstos.
- No continuar un flujo si faltan datos válidos.
- Definir la secuencia cuando una herramienta valida los datos que necesita la siguiente.
- Dar al usuario explicaciones, ejemplos y próximos pasos útiles.
- Reservar la derivación para excepciones, fallos repetidos o solicitudes explícitas.

El material también presenta dos extensiones que este ejercicio no implementa: usar `ToolContext` para compartir estado entre herramientas y envolver un agente especializado con `AgentTool`. Una función es preferible para operaciones determinísticas, como consultar un pedido; un agente como herramienta resulta útil cuando la subtarea requiere razonamiento especializado propio.

## Limitaciones de la demostración

- `ORDERS_DB` vive en memoria y contiene solamente tres pedidos ficticios.
- `process_refund` no cambia el estado ni registra que un pedido ya fue reembolsado; repetir la solicitud simula otro resultado exitoso.
- `escalate_to_supervisor` genera un ticket local, pero no crea un caso en un sistema externo.
- El ID del ticket se basa en `hash()`, por lo que puede cambiar al reiniciar Python.
- Los datos devueltos incluyen correos ficticios y no representan una estrategia de privacidad para producción.

En una aplicación real también serían necesarios autenticación, autorización, persistencia, idempotencia, auditoría y confirmaciones antes de ejecutar acciones con impacto económico.

## Archivos y ejecución

- `agent.py`: contiene la base de datos simulada, las tres herramientas y `root_agent`.
- `__init__.py`: permite que ADK cargue el paquete.

Configura `GOOGLE_API_KEY` en un archivo `.env` local y ejecuta, desde `adk-workspace`:

```bash
adk web
```

Luego selecciona `customer_support` en la interfaz y prueba las solicitudes anteriores.
