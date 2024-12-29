#!/usr/bin/env python
from dataclasses import area
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    danger_area = {
        "name": "Danger Area 1",
        "coordinates": [{"x": 52.5125, "y": 13.4125}],
        "status": "active",
        "dangerTypes": ["example_danger"],
    }

    relief_area = {
        "name": "Relief Area 1",
        "coordinates": [{"x": 52.5125, "y": 13.4125}],
        "status": "active",
        "reliefTypes": ["example_relief"],
    }

    dist_point = {
        "x": 52.5125,
        "y": 13.4125,
        "name": "Distribution Point 1",
        "resourcesList": ["example_resource"],
    }

    pickup_point = {
        "x": 52.5125,
        "y": 13.4125,
        "name": "Pickup Point 1",
        "pickupType": "example_pickup",
        "pickupDate": "2022-12-12",
        "transportCapacity": 10,
    }

    pois = f"addCustomMarker('map-marker', [{dist_point['y']}, {dist_point['x']}]);\naddCustomMarker('map-marker-alert', [{pickup_point['y']}, {pickup_point['x']}]);"
    area_coords = f"[{', '.join([f'[{coord['y']}, {coord['x']}]' for coord in area['coordinates']])}]"
    danger_area_coords = f"[{', '.join([f'[{coord['y']}, {coord['x']}]' for coord in danger_area['coordinates']])}]"
    relief_area_coords = f"[{', '.join([f'[{coord['y']}, {coord['x']}]' for coord in relief_area['coordinates']])}]"

    return render_template(
        "template.html",
        pois=pois,
        area_coords=area_coords,
        danger_area_coords=danger_area_coords,
        relief_area_coords=relief_area_coords,
    )


if __name__ == "__main__":
    app.run(debug=True)
