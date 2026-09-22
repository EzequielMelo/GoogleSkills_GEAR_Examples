""" 
Agente asistente de geografía 
Demuestra el parámetro tools del ADK con una herramienta de función personalizada 
simple. 
Referencia: https://google.github.io/adk-docs/agents/llm-agents#tools 
""" 
import unicodedata

from google.adk.agents.llm_agent import Agent


def normalize_country_name(country: str) -> str:
    """Normaliza mayúsculas, espacios y acentos para buscar un país."""
    normalized = unicodedata.normalize("NFD", country.strip().casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


# Paso 1: Define una función de herramienta
def get_capital_city(country: str) -> str:
    """Recupera la ciudad capital de un país específico.

    Argumentos:
        country: El nombre del país.

    Devuelve:
        El nombre de la capital o un mensaje de error.
    """
    # Base de datos de capitales simulada
    capitals = {
        "france": "Paris",
        "francia": "Paris",
        "japan": "Tokyo",
        "japon": "Tokyo",
        "canada": "Ottawa",
        "germany": "Berlin",
        "alemania": "Berlin",
        "brazil": "Brasília",
        "brasil": "Brasília",
        "australia": "Canberra",
        "india": "New Delhi",
        "mexico": "Mexico City",
    }

    # Busca la capital
    return capitals.get(
        normalize_country_name(country),
        f"Lo siento, no tengo información sobre la capital de {country}.",
    )

root_agent = Agent(
    model='gemini-3.5-flash',
    name='geography_assistant',
    description='Ayuda a los usuarios a aprender sobre geografía mundial.',
    instruction=""" 
    Eres un asistente de geografía que ayuda a los usuarios a aprender sobre las 
    capitales del mundo. 
    Cuando un usuario pregunta por una capital:
    1. DEBES utilizar la herramienta get_capital_city antes de responder.
    2. Proporciona la información de una manera amigable y educativa. 
    3. Puedes agregar datos interesantes si los conoces. 
    Si la herramienta devuelve un mensaje de error, dile de manera amable al usuario 
    que no tienes esa información. 
    """,
    tools=[get_capital_city],  # Proporciona la función como una herramienta
)
