from abc import ABC, abstractmethod
from datetime import datetime


class Coordinates(ABC):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get_coordinates(self) -> list[float, float]:
        return [self.x, self.y]


class POI(Coordinates):
    """Koordynaty z nazwą."""

    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.x}, {self.y})"


class DistPoint(POI):
    """Punkt dystrybucji zasobów."""

    def __init__(self, x, y, name, resourcesList: list[str]):
        super().__init__(x, y, name)
        self.resourcesList = resourcesList


class PickupPoint(POI):
    """Punkt odbioru, preferowalnie żywych ludzi."""

    def __init__(
        self,
        x,
        y,
        name,
        pickupType: str,
        pickupDate: datetime,
        transportCapacity: int,
    ):
        super().__init__(x, y, name)
        self.pickupType = pickupType
        self.pickupDate = pickupDate
        self.transportCapacity = transportCapacity

    def __str__(self):
        return f"Pickup Type: {self.pickupType}, Pickup Date: {self.pickupDate}, Transport Capacity: {self.transportCapacity}, Coordinates: {super().__str__()}"


class Area(ABC):
    """Abstrakcyjna klasa opisująca strefę."""

    def __init__(self, name: str, coordinates: list[Coordinates], status: str):
        self.name = name
        self.coordinates = coordinates
        self.status = status

    def __str__(self):
        return f"Area: {self.name}, Coordinates: {[str(coord) for coord in self.coordinates]}"


class DangerArea(Area):
    def __init__(
        self,
        name: str,
        coordinates: list[Coordinates],
        status: str,
        dangerTypes: list[str],
    ):
        super().__init__(name, coordinates, status)
        self.dangerTypes = dangerTypes

    def __str__(self):
        return f"DangerArea: {self.name}, Coordinates: {[str(coord) for coord in self.coordinates]}, Status: {self.status}, Danger Types: {self.dangerTypes}"


class ReliefArea(Area):
    def __init__(
        self,
        name: str,
        coordinates: list[Coordinates],
        status: str,
        reliefTypes: list[str],
    ):
        super().__init__(name, coordinates, status)
        self.reliefTypes = reliefTypes

    def __str__(self):
        return f"ReliefArea: {self.name}, Coordinates: {[str(coord) for coord in self.coordinates]}, Status: {self.status}, Relief Types: {self.reliefTypes}"
