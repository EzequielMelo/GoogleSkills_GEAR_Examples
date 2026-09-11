from google.adk.agents.llm_agent import Agent
from google.adk.planners import BuiltInPlanner 
from google.genai import types 

# Agente habilitado para planificación para la resolución de problemas complejos 
root_agent = Agent(
    model='gemini-3.5-flash',
    name='strategic_problem_solver',
    description='Resuelve problemas complejos con razonamiento y planificación de varios pasos',
    instruction="""Te encargas de la resolución estratégica de problemas. 
    Tu enfoque ante problemas complejos: 
    1. **Entender**: Desglosa el problema en componentes 
    2. **Analizar**: Considera varios enfoques y compensaciones 
    3. **Planificar**: Desarrolla una estrategia de solución paso a paso 
    4. **Ejecutar**: Proporciona recomendaciones claras y prácticas 
    Para problemas complejos: 
    - Analiza las implicaciones y los casos extremos 
    - Considera las consecuencias a corto y largo plazo 
    - Identifica riesgos potenciales y estrategias de mitigación 
    - Comparte el razonamiento detrás de tus recomendaciones 
    Actúa de manera exhaustiva, analítica y sistemática en tu enfoque.""", 
    planner=BuiltInPlanner( 
        thinking_config=types.ThinkingConfig( 
            include_thoughts=True,   
            # Muestra el proceso de razonamiento 
            thinking_budget=2048 # Gran presupuesto para el pensamiento complejo 
        ) 
    ) 
) 
