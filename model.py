# Models for the server
from pydantic import BaseModel
from typing import Set, Tuple, List, Optional

class ClientRequest(BaseModel):
    api_key: str = None
    lat: float = None
    lng: float = None

class EarthquakeData(BaseModel):
    magnitude: float = None
    location: str = None
    coordinates: Set[Tuple[float, float]] = set()
    time: float = None
    isTsunami: bool = None

class Alert(BaseModel):
    alert_level: int = None
    message: str = None
    remove_after: float = None
    disaster: str = None
    city: str = None

class ClientResponse(BaseModel):
    city_coordinates: Tuple[float, float] = set()
    alert_level: int = None
    number_of_alerts: int = None
    alerts: List = []