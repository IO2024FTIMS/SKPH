import openrouteservice

from flask import Blueprint, render_template

from app import db
from app.models.map import POI, DangerArea, ReliefArea, Coordinates


ORS_API_KEY = "Dodam_potem"
ors_client = openrouteservice.Client(key=ORS_API_KEY)

bp = Blueprint('maps', __name__,
               template_folder='../templates/maps',
               static_folder='static',
               static_url_path='maps')



@bp.route('/')
def index():
    TEST()

    # Filtrowanie po statusie jako boolean
    pois = POI.query.filter_by(status=True).all()
    danger_areas = DangerArea.query.filter_by(status=True).all()
    relief_areas = ReliefArea.query.filter_by(status=True).all()

    return render_template('map.jinja', pois=pois, danger_areas=danger_areas, relief_areas=relief_areas)

@bp.route('/<int:start_id>/<int:end_id>')
def get_route(start_id, end_id):
    # Sprawdź, czy punkt początkowy i końcowy istnieją w bazie danych
    start_poi = POI.query.get(start_id)
    end_poi = POI.query.get(end_id)

    if not start_poi or not end_poi:
        return {"error": "Invalid POI IDs"}, 404

    start_coords = [start_poi.coordinates.y, start_poi.coordinates.x]  # (y, x)
    end_coords = [end_poi.coordinates.y, end_poi.coordinates.x]  # (y, x)

    # Wyznacz trasę
    route_geometry = calculate_route(start_coords, end_coords)
    if route_geometry:
        return {"route": route_geometry}
    else:
        return {"error": "Unable to calculate route"}, 500

def TEST():
    # Dodawanie punktów POI
    coord1 = Coordinates(x=51.74708, y=19.45404)
    coord2 = Coordinates(x=51.74800, y=19.45500)
    db.session.add(coord1)
    db.session.add(coord2)

    poi1 = POI(name="Point A", coordinates=coord1, status=True)
    poi2 = POI(name="Point B", coordinates=coord2, status=True)
    db.session.add(poi1)
    db.session.add(poi2)

    # Dodanie pięciokątnej strefy zagrożenia
    pentagon_coords = [
        [51.7475, 19.4530],
        [51.7480, 19.4535],
        [51.7485, 19.4545],
        [51.7475, 19.4550],
        [51.7470, 19.4540]
    ]
    danger_area = DangerArea(name="Pentagon Danger Zone",
                             coordinates=pentagon_coords,
                             status=True)
    db.session.add(danger_area)

    # Dodanie dziewięciokątnej strefy pomocy
    nonagon_coords = [
        [51.7465, 19.4525],
        [51.7470, 19.4530],
        [51.7475, 19.4535],
        [51.7480, 19.4540],
        [51.7485, 19.4545],
        [51.7480, 19.4550],
        [51.7475, 19.4555],
        [51.7470, 19.4550],
        [51.7465, 19.4545]
    ]
    relief_area = ReliefArea(name="Nonagon Relief Zone",
                             coordinates=nonagon_coords,
                             status=True)
    db.session.add(relief_area)

    db.session.commit()

def calculate_route(start, end):
    """
    Wyznacz trasę między punktami start i end za pomocą OpenRouteService.
    """
    try:
        # Wywołanie API do obliczenia trasy
        route = ors_client.directions(
            coordinates=[start, end],
            profile='driving-car',  # Typ trasy: piesza, samochodowa, rowerowa
            format='geojson'
        )
        return route['features'][0]['geometry']  # Zwróć linię GeoJSON
    except Exception as e:
        print(f"Error calculating route: {e}")
        return None