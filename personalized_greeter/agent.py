""" 
Agente de bienvenida personalizado (demuestra las plantillas de estado) 
Muestra cómo la plantilla {var} inserta valores de estado en las instrucciones. 
Referencia: https://google.github.io/adk-docs/sessions/state 
"""

from google.adk.agents.llm_agent import Agent
from google.adk.agents.readonly_context import ReadonlyContext


def build_instruction(context: ReadonlyContext) -> str:
    """Construye las instrucciones usando el estado actual de la sesión."""
    user_name = context.state.get("user_name", "usuario")
    user_language = context.state.get("user_language", "English")
    membership_tier = context.state.get("membership_tier", "free")

    return f"""
    Eres un asistente amigable.
    Información del usuario:
    - Nombre: {user_name}
    - Idioma preferido: {user_language}
    - Membresía: {membership_tier}

    Tu nivel de membresía es: {membership_tier}.

    Saluda amablemente al usuario y ofrécele ayuda.
    Responde en {user_language}.
    """

root_agent = Agent(
    model='gemini-3.5-flash',
    name='personalized_greeter',
    instruction=build_instruction,
)
