from google.adk.agents.llm_agent import Agent

def search_flights(destination: str, date: str) -> dict:
    """" Searches for available flights to the specified destination on the given date. Returns a dictionary with flight details.
        Use this tool when the user asks for flight information.

        Args:
            destination (str): The destination city or airport code (e.g., 'Manila', 'Tokyo').
            date (str): The date of travel in YYYY-MM-DD format.
        
        Returns:
            dict: Flight search results.
                On success: {'status': 'success', 'flights': [list of flight details]},
                On failure: {'status': 'error', 'message': 'Error message describing the issue.'} 
    """
    available_flights = {
        "paris":[
            {"flight_number": "AF123", "departure_time": "2024-07-01T10:00:00", "duration_hours": "8", "price": 500},
            {"flight_number": "AF456", "departure_time": "2024-07-01T15:00:00", "duration_hours": "8", "price": 550},
        ],
        "tokyo": [
            {"flight_number": "JL789", "departure_time": "2024-07-01T12:00:00", "duration_hours": "14", "price": 800},
            {"flight_number": "JL101", "departure_time": "2024-07-01T18:00:00", "duration_hours": "14", "price": 850},
        ],
    }

    destination_key = destination.lower()

    if destination_key not in available_flights:
        return {"status": "error", "message": f"No flights found for destination: {destination}"}
    
    return {
        "status": "success",
        "flights": available_flights[destination_key],
        "destination": destination,
        "date": date,
        "count": len(available_flights[destination_key]),
    }

def search_hotels(destination: str, date: str) -> dict:
    """ Searches for available hotels in the specified destination on the given date. Returns a dictionary with hotel details.
        Use this tool when the user asks for hotel information.

        Args:
            destination (str): The destination city (e.g., 'Manila', 'Tokyo').
            date (str): The date of stay in YYYY-MM-DD format.
        
        Returns:
            dict: Hotel search results.
                On success: {'status': 'success', 'hotels': [list of hotel details]},
                On failure: {'status': 'error', 'message': 'Error message describing the issue.'} 
    """
    available_hotels = {
        "paris": [
            {"hotel_name": "Hotel Parisian", "check_in": "2024-07-01", "check_out": "2024-07-02", "price_per_night": 150},
            {"hotel_name": "Eiffel Stay", "check_in": "2024-07-01", "check_out": "2024-07-02", "price_per_night": 200},
        ],
        "tokyo": [
            {"hotel_name": "Tokyo Inn", "check_in": "2024-07-01", "price_per_night": 120},
            {"hotel_name": "Sakura Hotel", "check_in": "2024-07-01", "price_per_night": 180},
        ],
    }

    destination_key = destination.lower()

    if destination_key not in available_hotels:
        return {"status": "error", "message": f"No hotels found for destination: {destination}"}
    
    return {
        "status": "success",
        "hotels": available_hotels[destination_key],
        "destination": destination,
        "date": date,
        "count": len(available_hotels[destination_key]),
    }

def calculate_trip_cost(flight_cost: float, hotel_cost: float, num_nights: int) -> dict:
    """ Calculates the total cost of a trip based on flight and hotel costs. Returns a dictionary with the total cost.
        Use this tool when the user asks for trip cost information.

        Args:
            flight_cost (float): The cost of the flight.
            hotel_cost (float): The cost of the hotel stay.
            num_nights (int): The number of nights for the hotel stay.
        
        Returns:
            dict: Trip cost calculation results.
                On success: {'status': 'success', 'total_cost': total_cost, 'breakdown': {...}},
                On failure: {'status': 'error', 'message': 'Error message describing the issue.'} 
    """
    if flight_cost < 0 or hotel_cost < 0:
        return {"status": "error", "message": "Flight and hotel costs must be non-negative."}
    
    hotel_total_cost = hotel_cost * num_nights
    total_cost = flight_cost + hotel_total_cost

    return {
        "status": "success",
        "total_cost": total_cost,
        "flight_cost": flight_cost,
        "hotel_total_cost": hotel_total_cost,
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='travel_agent',
    description='Help users plan their trips by providing information about flights, hotels, and travel destinations.',
    instruction="""
        You are a travel agent. You can help users plan their trips by providing information about flights, hotels, 
        and travel destinations.

        Your capabilities include:
        1. Searching for available flights to a specified destination on a given date.
        2. Searching for available hotels in a specified destination on a given date.
        3. Calculating the total cost of a trip based on flight and hotel costs.
        4. Always present clear options to the user and ask for their preferences when necessary.
        5. If a tool returns an error, inform the user and ask for alternative options or inputs.

        When a user asks for flight information, use the `search_flights` tool.
        When a user asks for hotel information, use the `search_hotels` tool.
        When a user asks for trip cost information and full trip estimate, use the `calculate_trip_cost` tool.
    """,

    tools=[search_flights, search_hotels, calculate_trip_cost]
)
