import asyncio
from dotenv import load_dotenv

load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP_NAME = "name_extractor"
USER_ID = "test_user"
SESSION_ID = "test_session"

# 1. Configurar servicio y sesión inicial
session_service = InMemorySessionService()
session = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# 2. Turno 1: Extraer y almacenar en estado
user_message = Content(parts=[Part(text="Hi, my name is Alex Johnson")])
print("=== Running agent ===")
result = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message)

for event in result:
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"\nAgent response: {event.content.parts[0].text}")

# Refrescar la sesión desde session_service para obtener los cambios de output_key
session = asyncio.run(
    session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
)

print(f"\n=== State after execution ===")
print(f"Full state: {session.state}")
print(f"Extracted name: {session.state.get('user_name')}")

if session.state.get("user_name"):
    print("✅ Name was successfully extracted and stored!")
else:
    print("❌ Name extraction failed: No name found in the session state.")

# 3. Turno 2: Verificar persistencia de estado entre turnos
print("\n=== Simulating second turn ===")
result2 = runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=Content(parts=[Part(text="What's my name?")]),
)

for event in result2:
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Agent response: {event.content.parts[0].text}")

# Refrescar nuevamente para validar el estado
session = asyncio.run(
    session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
)

print(f"\nState still contains: {session.state.get('user_name')}")
if session.state.get("user_name"):
    print("✅ State persists across turns!")
else:
    print("❌ State did not persist.")
