from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field

# Paso 1: Define la estructura del resultado con Pydantic 
class ProductInfo(BaseModel): 
    product_name: str = Field(description="El nombre completo del producto") 
    price: float = Field(description="El precio en USD") 
    storage: str = Field(description="Capacidad de almacenamiento (p. ej., '256GB')") 
    color: str = Field(default="No se especifica", description="Color del producto, si se menciona") 

root_agent = Agent(
    model='gemini-3.5-flash',
    name='product_extractor',
    description='"Extrae información del producto de los mensajes del usuario y devuelve un objeto JSON estructurado',
    instruction="""Eres un extractor de información de productos. 
Tu tarea: 
- Lee el mensaje del usuario sobre un producto 
- Extrae product_name, price, storage y color (si se mencionan) 
- Responde SOLO con un objeto JSON válido que coincida con este formato: 
{ 
    "product_name": "product name here", 
    "price": 999.99, 
    "storage": "256GB", 
    "color": "titanio negro" 
} 
Reglas: 
- El precio debe ser un número (sin signos de dólar) 
- El almacenamiento debe incluir la unidad (como GB o TB) 
- Si no se menciona el color, se debe utilizar "No se especifica" 
- SOLO se debe devolver el objeto JSON como resultado, sin ningún texto explicativo""", 
output_schema=ProductInfo,  # Aplica esta estructura exacta 
output_key="extracted_product"  # Almacena el resultado en el estado de la sesión 
)
