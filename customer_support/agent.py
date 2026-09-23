"""
Agente de asistencia al cliente con herramientas coordinadas.
Demuestra la combinación estratégica de herramientas y el manejo de errores.
Referencia: https://google.github.io/adk-docs/tools-custom/
"""

from google.adk.agents.llm_agent import Agent


ORDERS_DB = {
    "ORD123": {
        "status": "shipped",
        "total": 99.99,
        "customer": "john@email.com",
    },
    "ORD456": {
        "status": "processing",
        "total": 149.99,
        "customer": "jane@email.com",
    },
    "ORD789": {
        "status": "delivered",
        "total": 249.99,
        "customer": "bob@email.com",
    },
}


def check_order_status(order_id: str) -> dict:
    """Comprueba el estado actual del pedido de un cliente.

    Utiliza esta herramienta cuando un cliente pregunte por el estado de su pedido
    o la entrega.

    Argumentos:
        order_id: El ID de pedido (p. ej., "ORD123").

    Devuelve:
        Información del pedido o un error con tipo y mensaje.
    """
    if not order_id.startswith("ORD"):
        return {
            "status": "error",
            "error_type": "invalid_format",
            "error_message": (
                "Los IDs de pedido deben comenzar con 'ORD' (p. ej., ORD123)"
            ),
        }

    if order_id not in ORDERS_DB:
        return {
            "status": "error",
            "error_type": "not_found",
            "error_message": f"El pedido {order_id} no se encontró en el sistema",
        }

    order = ORDERS_DB[order_id]
    return {
        "status": "success",
        "order_id": order_id,
        "order_status": order["status"],
        "details": order,
    }


def process_refund(order_id: str, reason: str) -> dict:
    """Procesa una solicitud de reembolso de un pedido.

    Utiliza esta herramienta solo después de verificar que el pedido existe con
    `check_order_status`.

    Argumentos:
        order_id: El ID de pedido que se desea reembolsar.
        reason: El motivo del cliente para solicitar el reembolso.

    Devuelve:
        El resultado del reembolso o un error con tipo y mensaje.
    """
    if order_id not in ORDERS_DB:
        return {
            "status": "error",
            "error_type": "order_not_found",
            "error_message": (
                "No se puede procesar el reembolso: "
                f"no se encontró el pedido {order_id}"
            ),
        }

    order = ORDERS_DB[order_id]

    if order["status"] == "delivered":
        return {
            "status": "success",
            "refund_amount": order["total"],
            "reference": f"REF{order_id[3:]}",
            "estimated_days": 5,
            "reason": reason,
            "message": "Reembolso procesado de manera exitosa",
        }

    return {
        "status": "error",
        "error_type": "cannot_refund",
        "error_message": (
            f"No se puede reembolsar el pedido en el estado '{order['status']}'. "
            "Solo se podrán reembolsar los pedidos entregados."
        ),
    }


def escalate_to_supervisor(issue_summary: str, order_id: str) -> dict:
    """Deriva problemas complejos a un supervisor humano.

    Utiliza esta herramienta cuando el problema no pueda resolverse con las demás
    herramientas o cuando el cliente pida hablar con un supervisor.

    Argumentos:
        issue_summary: Resumen breve del problema.
        order_id: ID de pedido relacionado, si corresponde.

    Devuelve:
        La confirmación de la derivación y el ID del ticket.
    """
    ticket_id = f"TICKET{hash(issue_summary) % 10000:04d}"

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": "Problema derivado al supervisor",
        "estimated_response": "en 2 horas",
        "order_id": order_id if order_id else "N/A",
    }


root_agent = Agent(
    model="gemini-3.5-flash",
    name="customer_support_agent",
    description=(
        "Maneja consultas de clientes sobre pedidos y reembolsos con manejo "
        "integral de errores."
    ),
    instruction="""
    Eres un agente de asistencia al cliente servicial y empático para una empresa de
    comercio electrónico.

    # Tus capacidades

    Tienes tres herramientas disponibles:
    1. check_order_status(order_id): verifica el estado de un pedido.
    2. process_refund(order_id, reason): procesa solicitudes de reembolso.
    3. escalate_to_supervisor(issue_summary, order_id): deriva problemas complejos.

    # Lineamientos para el flujo de trabajo

    ## Consultas sobre el estado del pedido

    1. Saluda al cliente de manera cálida.
    2. Utiliza check_order_status con el ID que proporcione.
    3. Si status='success', proporciona una actualización clara con detalles.
    4. Si error_type='not_found', pide que verifique el ID.
    5. Si error_type='invalid_format', explica que los IDs comienzan con "ORD".

    ## Solicitudes de reembolso

    1. Expresa empatía por la situación.
    2. Primero usa check_order_status para verificar que el pedido exista.
    3. Si no existe, solicita al cliente que verifique el ID y no continúes.
    4. Si existe, utiliza process_refund con el ID y el motivo.
    5. Si el reembolso tiene éxito, confirma la referencia, el importe y el plazo.
    6. Si error_type='cannot_refund', explica la política y ofrece una derivación.

    ## Estrategia de manejo de errores

    - Para 'not_found', solicita que se revise el ID y ofrece ayudar de nuevo.
    - Para 'invalid_format', explica el formato y proporciona el ejemplo ORD123.
    - Para 'cannot_refund', explica que solo se reembolsan pedidos entregados y
      ofrece derivar el caso si el cliente solicita una excepción.

    ## Cuándo realizar una derivación

    Utiliza escalate_to_supervisor cuando:
    - El cliente solicita hablar con un supervisor o gerente.
    - El problema no puede resolverse con las herramientas disponibles.
    - El cliente solicita una excepción a la política.
    - Varios intentos de usar una herramienta fallaron.

    Después de la derivación, proporciona el ID del ticket, informa el tiempo de
    respuesta esperado y agradece al cliente por su paciencia.

    # Estilo de comunicación

    Sé educado, profesional y empático. Indica los próximos pasos con claridad,
    reconoce los sentimientos del cliente y no hagas promesas que no puedas cumplir.
    """,
    tools=[check_order_status, process_refund, escalate_to_supervisor],
)
