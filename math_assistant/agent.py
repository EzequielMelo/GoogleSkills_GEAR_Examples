""" 
Agente asistente de matemáticas 
Demuestra la herramienta integrada de ejecución de código del ADK para realizar 
cálculos. 
Referencia: https://google.github.io/adk-docs/tools/built-in-tools#code-execution 
""" 

from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor  # Importa el ejecutor de código 

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='Ayuda a los usuarios con cálculos y análisis matemáticos.',
    instruction=""" 
    Eres un asistente de matemáticas que ayuda a los usuarios con cálculos y análisis 
    matemáticos. 
    Tus capacidades: 
    1. Cuando los usuarios pidan cálculos, utiliza la ejecución de código para mayor 
    precisión. 
    2. Muestra tu trabajo explicando los pasos del cálculo. 
    3. Verifica los resultados ejecutando el código. 
    4. Realiza operaciones matemáticas complejas (estadísticas, álgebra, etc.). 
    Utiliza siempre la ejecución de código para cálculos numéricos para garantizar la 
    exactitud. 
    """,
    code_executor=BuiltInCodeExecutor()  # Habilita la ejecución de código
)
