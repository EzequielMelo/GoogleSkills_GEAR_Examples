""" 
Agente de asistente de investigación 
Demuestra la herramienta integrada de la Búsqueda de Google del ADK para obtener 
información en tiempo real. 
Referencia: https://google.github.io/adk-docs/tools/built-in-tools#google-search 
""" 

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search  # Importa la herramienta Búsqueda de Google 

root_agent = Agent(
    model='gemini-3.5-flash',
    name='research_assistant',
    description='Ayuda a los usuarios a investigar temas con la Búsqueda de Google.',
    instruction=""" 
    Eres un asistente de investigación que ayuda a los usuarios a encontrar 
    información precisa y actualizada. 
    Tu enfoque: 
    1. Cuando los usuarios hagan preguntas que requieran información actual, utiliza 
    la Búsqueda de Google 
    2. Basa tus respuestas en los resultados de la búsqueda 
    3. Cita fuentes cuando proporciones información 
    4. Si los resultados de la búsqueda son insuficientes, reconoce las limitaciones 
    Prioriza siempre la exactitud sobre la especulación. Si no estás seguro, dilo. 
    """,
    tools=[google_search]  # Habilita la fundamentación de la Búsqueda de Google
)
