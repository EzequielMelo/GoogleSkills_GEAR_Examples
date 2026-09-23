"""
Agente de viajes con herramientas de funciones personalizadas.
Demuestra varias herramientas personalizadas que funcionan en conjunto.
Referencia: https://google.github.io/adk-docs/tools-custom/function-tools/
"""

import unicodedata

from google.adk.agents.llm_agent import Agent


def normalize_city_name(city: str) -> str:
    """Normaliza espacios, mayúsculas y acentos de un nombre de ciudad."""
    normalized = unicodedata.normalize("NFD", city.strip().casefold())
    normalized = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )
    aliases = {
        "paris": "paris",
        "tokio": "tokyo",
        "tokyo": "tokyo",
    }
    return aliases.get(normalized, normalized)


# Herramienta 1: Busca vuelos
def search_flights(destination: str, departure_date: str) -> dict:
    """Busca vuelos disponibles a un destino en una fecha específica.

    Utiliza esta herramienta cuando un cliente quiera saber las opciones de vuelo.

    Argumentos:
        destination: La ciudad de destino (p. ej., "París", "Tokio").
        departure_date: Fecha de salida en formato AAAA-MM-DD.

    Devuelve:
        Resultados de la búsqueda de vuelos. En caso de éxito devuelve
        ``{'status': 'success', 'flights': [...], 'count': N}``. En caso de
        error devuelve ``{'status': 'error', 'error_message': 'explanation'}``.
    """
    available_flights = {
        "paris": [
            {"flight_number": "AF123", "price_usd": 450, "duration_hours": 8},
            {"flight_number": "BA456", "price_usd": 480, "duration_hours": 7.5},
        ],
        "tokyo": [
            {"flight_number": "JL789", "price_usd": 850, "duration_hours": 13},
            {"flight_number": "ANA101", "price_usd": 820, "duration_hours": 12.5},
        ],
    }

    dest_key = normalize_city_name(destination)
    if dest_key not in available_flights:
        return {
            "status": "error",
            "error_message": (
                f"No se encontraron vuelos a {destination}. Prueba París o Tokio."
            ),
        }

    return {
        "status": "success",
        "destination": destination,
        "departure_date": departure_date,
        "flights": available_flights[dest_key],
        "count": len(available_flights[dest_key]),
    }


# Herramienta 2: Busca hoteles
def search_hotels(city: str, check_in_date: str) -> dict:
    """Busca hoteles disponibles en una ciudad para una fecha de entrada.

    Utiliza esta herramienta cuando un cliente necesite alojamiento.

    Argumentos:
        city: El nombre de la ciudad (p. ej., "París", "Tokio").
        check_in_date: La fecha de entrada en formato AAAA-MM-DD.

    Devuelve:
        Resultados de la búsqueda de hoteles. En caso de éxito devuelve
        ``{'status': 'success', 'hotels': [...], 'count': N}``. En caso de
        error devuelve ``{'status': 'error', 'error_message': 'explanation'}``.
    """
    available_hotels = {
        "paris": [
            {"name": "Hotel Eiffel", "price_per_night_usd": 150, "rating": 4.5},
            {"name": "Louvre Inn", "price_per_night_usd": 120, "rating": 4.2},
        ],
        "tokyo": [
            {"name": "Shibuya Grand", "price_per_night_usd": 180, "rating": 4.7},
            {"name": "Tokyo Bay Hotel", "price_per_night_usd": 140, "rating": 4.3},
        ],
    }

    city_key = normalize_city_name(city)
    if city_key not in available_hotels:
        return {
            "status": "error",
            "error_message": (
                f"No se encontraron hoteles en {city}. Prueba París o Tokio."
            ),
        }

    return {
        "status": "success",
        "city": city,
        "check_in_date": check_in_date,
        "hotels": available_hotels[city_key],
        "count": len(available_hotels[city_key]),
    }


# Herramienta 3: Calcula el presupuesto del viaje
def calculate_trip_budget(
    flight_price: float,
    hotel_price: float,
    num_nights: int,
) -> dict:
    """Calcula el presupuesto total del viaje con vuelo y alojamiento.

    Utiliza esta herramienta después de encontrar los precios de vuelos y hoteles
    para darle al cliente una estimación total.

    Argumentos:
        flight_price: Costo del vuelo de ida y vuelta en USD.
        hotel_price: Costo del hotel por noche en USD.
        num_nights: Número de noches de hospedaje.

    Devuelve:
        Un diccionario con el total y su desglose.
    """
    hotel_total = hotel_price * num_nights
    total = flight_price + hotel_total

    return {
        "status": "success",
        "total_usd": round(total, 2),
        "breakdown": {
            "flight_cost": flight_price,
            "hotel_cost_per_night": hotel_price,
            "num_nights": num_nights,
            "hotel_total": round(hotel_total, 2),
        },
    }


root_agent = Agent(
    model="gemini-3.5-flash",
    name="travel_agent",
    description="Ayuda a los usuarios a planificar viajes buscando vuelos y hoteles.",
    instruction="""
    Eres un asesor de viajes servicial.

    Tus capacidades:
    - Buscar vuelos con search_flights(destination, departure_date)
    - Buscar hoteles con search_hotels(city, check_in_date)
    - Calcular presupuestos de viaje con calculate_trip_budget(
      flight_price, hotel_price, num_nights)

    Cuando ayudes a los usuarios:
    1. Si preguntan por vuelos, utiliza search_flights.
    2. Si preguntan por hoteles, utiliza search_hotels.
    3. Si desean una estimación completa del viaje, utiliza ambas herramientas de
       búsqueda y, a continuación, calculate_trip_budget.
    4. Presenta siempre las opciones de manera clara con los precios.
    5. Si una herramienta devuelve un error, pide disculpas y sugiere destinos
       disponibles (París o Tokio).

    Sé amable y ayuda a los usuarios a planificar su viaje perfecto.
    """,
    tools=[search_flights, search_hotels, calculate_trip_budget],
)
