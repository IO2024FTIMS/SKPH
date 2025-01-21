from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.extensions import db

class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinates({self.x}, {self.y})"

class POI(db.Model):
    __tablename__ = 'poi'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    coordinates_id = Column(Integer, ForeignKey('coordinates.id'))
    coordinates = relationship('Coordinates', backref='poi')  # change backref to 'poi' for clarity

    def __init__(self, name: str, coordinates: Coordinates):
        self.name = name
        self.coordinates = coordinates

    def __repr__(self):
        return f"{self.name} ({self.coordinates.x}, {self.coordinates.y})"

class DangerArea(db.Model):
    __tablename__ = 'danger_area'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    coordinates = Column(JSON)  # Przechowuje listę współrzędnych

    def __init__(self, name: str, coordinates: list, status: str):
        self.name = name
        self.coordinates = coordinates
        self.status = status

    def __repr__(self):
        return f"DangerArea({self.name}, {self.status})"

class ReliefArea(db.Model):
    __tablename__ = 'relief_area'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    coordinates = Column(JSON)  # Przechowuje listę współrzędnych

    def __init__(self, name: str, coordinates: list, status: str):
        self.name = name
        self.coordinates = coordinates
        self.status = status

    def __repr__(self):
        return f"ReliefArea({self.name}, {self.status})"
