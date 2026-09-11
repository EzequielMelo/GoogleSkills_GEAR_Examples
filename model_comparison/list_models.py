import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

print("Modelos habilitados para generateContent en tu cuenta:")
for m in client.models.list():
    if "generateContent" in (m.supported_actions or []):
        # Limpia el prefijo 'models/' para ver el nombre directo
        name = m.name.replace("models/", "")
        print(f" - {name}")