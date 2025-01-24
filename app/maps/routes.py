import openrouteservice
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.auth.user_service import roles_required
from app.extensions import db
from app.models.map import POI, DangerArea, ReliefArea, Coordinates

ORS_API_KEY = "api"
ors_client = openrouteservice.Client(key=ORS_API_KEY)

bp = Blueprint(
    "maps",
    __name__,
    template_folder="../templates/maps",
    static_folder="static",
    static_url_path="maps",
)


@bp.route("/")
def index():

    pois = POI.query.filter_by(status=True).all()
    danger_areas = DangerArea.query.filter_by(status=True).all()
    relief_areas = ReliefArea.query.filter_by(status=True).all()

    return render_template(
        "map.jinja",
        pois=pois,
        danger_areas=danger_areas,
        relief_areas=relief_areas,
    )


@bp.route("/add")
@roles_required(["admin", "organization"])
def add_page():

    pois = POI.query.filter_by(status=True).all()
    danger_areas = DangerArea.query.filter_by(status=True).all()
    relief_areas = ReliefArea.query.filter_by(status=True).all()

    return render_template(
        "bare-map.jinja",
        pois=pois,
        danger_areas=danger_areas,
        relief_areas=relief_areas,
    )


# API stuff
@bp.route("/<int:start_id>/<int:end_id>")
def get_route(start_id, end_id):
    start_poi = POI.query.get(start_id)
    end_poi = POI.query.get(end_id)

    if not start_poi or not end_poi:
        return {"error": "Invalid POI IDs"}, 404

    start_coords = [start_poi.coordinates.y, start_poi.coordinates.x]
    end_coords = [end_poi.coordinates.y, end_poi.coordinates.x]

    route_geometry = calculate_route(start_coords, end_coords)
    if route_geometry:
        return {"route": route_geometry}
    else:
        return {"error": "Unable to calculate route"}, 500


@bp.route("/add-poi", methods=["POST"])
def add_poi():
    data = request.get_json()
    lat = data["lat"]
    lng = data["lng"]
    name = data.get("name", "Unnamed POI")
    type_of_poi = data.get("type")

    coordinates = Coordinates(x=lat, y=lng)
    db.session.add(coordinates)
    poi = POI(
        name=name,
        coordinates=coordinates,
        type_of_poi=type_of_poi,
        status=True,
    )
    db.session.add(poi)
    db.session.commit()

    pois = POI.query.filter_by(status=True).all()

    return jsonify(
        {
            "success": True,
            "pois": [
                {"id": poi.id, "name": poi.name, "type": poi.type_of_poi}
                for poi in pois
            ],
        }
    )


@bp.route("/add-danger-area", methods=["POST"])
def add_danger_area():
    data = request.get_json()
    coordinates = data["coordinates"]
    name = data.get("name", "Unnamed Danger Area")

    danger_area = DangerArea(name=name, coordinates=coordinates, status=True)
    db.session.add(danger_area)
    db.session.commit()

    danger_areas = DangerArea.query.filter_by(status=True).all()

    return jsonify(
        {
            "success": True,
            "danger_areas": [
                {"id": area.id, "name": area.name} for area in danger_areas
            ],
        }
    )


@bp.route("/add-relief-area", methods=["POST"])
def add_relief_area():
    data = request.get_json()
    coordinates = data["coordinates"]
    name = data.get("name", "Unnamed Relief Area")

    relief_area = ReliefArea(name=name, coordinates=coordinates, status=True)
    db.session.add(relief_area)
    db.session.commit()

    relief_areas = ReliefArea.query.filter_by(status=True).all()

    return jsonify(
        {
            "success": True,
            "relief_areas": [
                {"id": area.id, "name": area.name} for area in relief_areas
            ],
        }
    )


@bp.route("/delete-poi/<int:poi_id>", methods=["DELETE"])
def delete_poi(poi_id):
    poi = POI.query.get(poi_id)
    if poi:
        db.session.delete(poi)
        db.session.commit()
        return jsonify(
            {"success": True, "message": "POI deleted successfully"}
        )
    else:
        return jsonify({"success": False, "message": "POI not found"}), 404


@bp.route("/delete-danger-area/<int:area_id>", methods=["DELETE"])
def delete_danger_area(area_id):
    area = DangerArea.query.get(area_id)
    if area:
        db.session.delete(area)
        db.session.commit()
        return jsonify(
            {"success": True, "message": "Danger Area deleted successfully"}
        )
    else:
        return (
            jsonify({"success": False, "message": "Danger Area not found"}),
            404,
        )


@bp.route("/delete-relief-area/<int:area_id>", methods=["DELETE"])
def delete_relief_area(area_id):
    area = ReliefArea.query.get(area_id)
    if area:
        db.session.delete(area)
        db.session.commit()
        return jsonify(
            {"success": True, "message": "Relief Area deleted successfully"}
        )
    else:
        return (
            jsonify({"success": False, "message": "Relief Area not found"}),
            404,
        )


def calculate_route(start, end):
    try:
        route = ors_client.directions(
            coordinates=[start, end], profile="driving-car", format="geojson"
        )
        return route["features"][0]["geometry"]
    except RuntimeError as e:
        print(f"Error calculating route: {e}")
        return None
