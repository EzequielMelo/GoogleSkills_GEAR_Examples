""" 
Prueba crear plantillas de estado con diferentes valores. 
Ejecútalo con: python test_templating.py 
""" 
import asyncio

from dotenv import load_dotenv

load_dotenv()

from agent import root_agent 
from google.adk.runners import Runner 
from google.adk.sessions import InMemorySessionService 
from google.genai.types import Content, Part 

# Establece la configuración 
APP_NAME = root_agent.name
USER_ID = "user1"

session_service = InMemorySessionService() 
asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id="session1" 
))
runner = Runner( 
    agent=root_agent, 
    app_name=APP_NAME,
    session_service=session_service 
) 

# Prueba 1: No hay estado establecido (todos los valores predeterminados) 
print("=== Prueba 1: Sin estado (todos los valores predeterminados) ===") 
result1 = runner.run( 
    user_id=USER_ID,
    session_id="session1", 
    new_message=Content(parts=[Part(text="Hola")]) 
) 
for event in result1: 
    if event.is_final_response() and event.content and event.content.parts:
        print(f"Agente: {event.content.parts[0].text}\n") 

# Prueba 2: Establece solo el nombre de usuario 
print("=== Prueba 2: Con nombre de usuario ===") 
asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id="session2",
    state={"user_name": "Álex"},
))
result2 = runner.run( 
    user_id=USER_ID,
    session_id="session2", 
    new_message=Content(parts=[Part(text="Hola de nuevo")]) 
) 
for event in result2: 
    if event.is_final_response() and event.content and event.content.parts:
        print(f"Agente: {event.content.parts[0].text}\n") 

# Prueba 3: Establece todos los valores de estado 
print("=== Prueba 3: Con todos los valores de estado ===") 
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id="session3",
    state={
        "user_name": "Álex",
        "user_language": "Spanish",
        "membership_tier": "premium",
    },
))
result3 = runner.run( 
    user_id=USER_ID,
    session_id="session3", 
    new_message=Content(parts=[Part(text="Hola de nuevo")]) 
) 
for event in result3: 
    if event.is_final_response() and event.content and event.content.parts:
        print(f"Agente: {event.content.parts[0].text}\n") 

print("=== Estado actual ===") 
print(session.state) 
