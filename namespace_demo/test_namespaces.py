"""Prueba las diferencias de persistencia entre namespaces de estado."""

import asyncio

from dotenv import load_dotenv

load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP_NAME = root_agent.name
USER_ID = "user1"


def get_session(session_service, session_id):
    """Obtiene una copia actualizada de una sesión."""
    return asyncio.run(
        session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    )


def print_final_response(events):
    """Imprime la respuesta final si el evento contiene texto."""
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Respuesta del agente:\n{event.content.parts[0].text}\n")


session_service = InMemorySessionService()
session = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="session1",
        state={
            "app:name": "Demostración de espacios de nombres",
            "app:version": "2.0",
            "user:theme": "dark",
            "topic": "state management",
        },
    )
)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

print("=== Estado antes del turno 1 ===")
print(session.state)

print("\n=== Agente en ejecución (turno 1) ===")
print_final_response(
    runner.run(
        user_id=USER_ID,
        session_id="session1",
        new_message=Content(
            parts=[Part(text="Muéstrame los valores de los espacios de nombres")]
        ),
    )
)

session = get_session(session_service, "session1")
print("=== Estado persistido después del turno 1 ===")
print(f"Estado completo: {session.state}")
print(f"temp:step: {session.state.get('temp:step')} (descartado)")
print(f"topic: {session.state.get('topic')} (persiste en la sesión)")
print(f"user:theme: {session.state.get('user:theme')} (persiste para el usuario)")
print(f"app:version: {session.state.get('app:version')} (persiste en la app)")

print("\n=== Turno 2 (misma sesión) ===")
print_final_response(
    runner.run(
        user_id=USER_ID,
        session_id="session1",
        new_message=Content(parts=[Part(text="Vuelve a verificar el estado")]),
    )
)

session = get_session(session_service, "session1")
print("=== Estado persistido después del turno 2 ===")
print(f"temp:step: {session.state.get('temp:step')} (descartado nuevamente)")
print(f"topic: {session.state.get('topic')} (continúa en la sesión)")

print("\n=== Nueva sesión para el mismo usuario ===")
session2 = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="session2",
    )
)

print(f"Estado de la nueva sesión: {session2.state}")
print(f"topic: {session2.state.get('topic')} (descartado con session1)")
print(f"user:theme: {session2.state.get('user:theme')} (heredado por el usuario)")
print(f"app:version: {session2.state.get('app:version')} (heredado por la app)")
