from typing import Any, Dict, List, Optional, Tuple, Union
from FlightRadar24 import FlightRadar24API
from FlightRadar24.entities.flight import Flight

class CustomFlightRadarAPI(FlightRadar24API):
    def __init__(self, user: Optional[str] = None, password: Optional[str] = None, custom_param: Optional[str] = None):
        """
        Constructor of the CustomFlightRadarAPI class.

        :param user: Your email (optional)
        :param password: Your password (optional)
        :param custom_param: A custom parameter for additional functionality (optional)
        """
        super().__init__(user, password)
        self.custom_param = custom_param

    def get_flight(self, airline: Optional[str] = None, flight_number: Optional[str] = None):
        flights = self.get_flights(airline=airline, flight_number=flight_number)
        if (flights):
            return flights[0]
        print("This is a custom method.")

    def get_flights(
        self,
        airline: Optional[str] = None,
        bounds: Optional[str] = None,
        registration: Optional[str] = None,
        aircraft_type: Optional[str] = None,
        destination: Optional[str] = None,
        flight_number: Optional[str] = None,
        *,
        details: bool = False
    ) -> List[Flight]:
        """
        Override an existing method to customize its behavior.
        """
        # Call the parent method if needed
        flights = super().get_flights(
            airline=airline,
            bounds=bounds,
            registration=registration,
            aircraft_type=aircraft_type,
            details=details
        )
        if flight_number:
            flights = [flight for flight in flights if flight.number == flight_number or flight.callsign == flight_number]
            if flights:
                return flights
        if destination:
            flights = [flight for flight in flights if flight.destination_airport_iata == destination]
        # Add custom behavior here
        print("Custom behavior for getting flight data.")
        return flights