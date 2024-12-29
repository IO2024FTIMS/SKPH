from dataClasses import (
    POI,
    DistPoint,
    PickupPoint,
    ReliefArea,
    DangerArea,
    Coordinates,
)
from flask import Flask, render_template, jsonify
import datetime
import json

app = Flask(__name__)

# Sample data
dist_points = [
    DistPoint(
        1.23456789, 10.12345678, "distPoint1", ["resource1", "resource2"]
    ),
    DistPoint(
        2.34567890, 11.23456789, "distPoint2", ["resource3", "resource4"]
    ),
]
pickup_points = [
    PickupPoint(
        3.45678901,
        12.34567890,
        "Pickup1",
        "human",
        datetime.datetime.now(),
        10,
    ),
    PickupPoint(
        4.56789012,
        13.45678901,
        "Pickup2",
        "animal",
        datetime.datetime.now(),
        5,
    ),
]
areas = [
    DangerArea(
        "danger",
        [Coordinates(3.5, 12.5), Coordinates(4.5, 13.5)],
        "active",
        ["danger_type_1", "danger_type_2"],
    ),
    ReliefArea(
        "relief",
        [Coordinates(2.5, 11.5), Coordinates(5.5, 14.5)],
        "active",
        ["relief_type_1", "relief_type_2"],
    ),
]


@app.route("/")
def index():
    # Convert data to JSON format
    dist_points_json = [dist_point.to_dict() for dist_point in dist_points]
    pickup_points_json = [
        pickup_point.to_dict() for pickup_point in pickup_points
    ]
    areas_json = [area.to_dict() for area in areas]

    return render_template(
        "map.html",
        dist_points=dist_points_json,
        pickup_points=pickup_points_json,
        areas=areas_json,
    )


@app.route("/data")
def data():
    # Convert data to JSON format and send it as response
    dist_points_json = [dist_point.to_dict() for dist_point in dist_points]
    pickup_points_json = [
        pickup_point.to_dict() for pickup_point in pickup_points
    ]
    areas_json = [area.to_dict() for area in areas]

    return jsonify(
        {
            "dist_points": dist_points_json,
            "pickup_points": pickup_points_json,
            "areas": areas_json,
        }
    )


def Coordinates(self, x: float, y: float):
    # Add this method to your Coordinates class in dataClasses.py
    self.x = x
    self.y = y


def __str__(self):
    # Update the __str__ method in your Coordinates class in dataClasses.py
    return f"Coordinates({self.x}, {self.y})"


def to_dict(self):
    # Add this method to your classes in dataClasses.py
    fields = [field for field in vars(self) if not field.startswith("__")]
    return {field: getattr(self, field) for field in fields}


if __name__ == "__main__":
    app.run(debug=True)
