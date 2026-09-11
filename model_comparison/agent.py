""" 
Demostración de configuración de modelos   que muestra la optimización fáctica frente 
a la optimización creativa.  
Demuestra generate_content_config del ADK con diferente configuración. 
"""

from google.adk.agents.llm_agent import Agent
from google.genai import types

# Agente 1: Optimizado para la extracción de datos fácticos 
# Utiliza una temperatura baja para una mayor coherencia y seguridad estricta en pos de la exactitud 

factual_agent = Agent(
    model='gemini-3.5-flash',
    name='data_extractor',
    description='Extrae información fáctica de forma sumamente coherente',
    instruction="""Eres un extractor de datos precisos. 
    Extrae hechos exactamente como se indica. No hagas lo siguiente: 
    - Agregar información que no figure en la entrada 
    - Hacer suposiciones o inferencias 
    - Usar lenguaje creativo 
    Sé preciso, conciso y determinístico.""", 
    generate_content_config=types.GenerateContentConfig( 
        temperature=0.1,  # Muy baja para mantener la coherencia 
        max_output_tokens=500, 
        top_p=0.8, 
        top_k=10, 
        safety_settings=[ 
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, 
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE 
            ) 
        ] 
    )    
) 

# Agente 2: Optimizado para la generación de ideas creativas 
# Utiliza una temperatura alta para promover la creatividad y el modelo Pro para generar mejores ideas

creative_agent = Agent(
    model='gemini-3.1-pro-preview',
    name='creative_brainstormer',
    description='Genera ideas creativas y explora posibilidades innovadoras',
    instruction="""Eres un socio de generación de ideas creativo. 
    Genera ideas innovadoras, diversas y originales.  Puedes hacer lo siguiente: 
    - Pensar de forma creativa 
    - Combinar conceptos inesperados 
    - Explorar enfoques no convencionales 
    Sé creativo, ofrece distintas opciones y fomenta la reflexión.""", 
    generate_content_config=types.GenerateContentConfig( 
        temperature=0.9,  # Alta para una mayor creatividad 
        max_output_tokens=2000,  # Permite ideas detalladas 
        top_p=0.95, 
        top_k=40, 
        safety_settings=[ 
            types.SafetySetting( 
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, 
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE 
            ) 
        ] 
    ) 
) 

# Para el ADK web, utilizaremos el agente fáctico como agente raíz 
# Cambia a creative_agent para probar un comportamiento diferente 
root_agent = creative_agent

