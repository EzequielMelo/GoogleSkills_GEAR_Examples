"""Agente que demuestra los espacios de nombres del estado en Google ADK."""

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
from google.adk.agents.readonly_context import ReadonlyContext


def set_temporary_state(callback_context: CallbackContext) -> None:
    """Crea un valor disponible solamente durante la invocación actual."""
    callback_context.state["temp:step"] = "initialization"


def build_instruction(context: ReadonlyContext) -> str:
    """Construye las instrucciones con el estado visible en la sesión actual."""
    app_name = context.state.get(
        "app:name", "Demostración de espacios de nombres"
    )
    app_version = context.state.get("app:version", "1.0")
    user_theme = context.state.get("user:theme", "not set")
    topic = context.state.get("topic", "not set")
    current_step = context.state.get("temp:step", "not set")

    return f"""
    Eres un asistente de demostración que muestra los espacios de nombres de estado.

    === Estado de la app (global para todos los usuarios) ===
    Nombre de la app: {app_name}
    Versión de la app: {app_version}

    === Estado del usuario (persiste entre sesiones) ===
    Preferencia del usuario: {user_theme}

    === Estado de la sesión (persiste en esta conversación) ===
    Tema de conversación: {topic}

    === Estado temporal (solo durante la invocación actual) ===
    Paso actual: {current_step}

    Responde con un mensaje amigable mostrando estos valores.
    """


root_agent = Agent(
    model="gemini-3.5-flash",
    name="namespace_demo",
    instruction=build_instruction,
    before_agent_callback=set_temporary_state,
    output_key="response",
)
