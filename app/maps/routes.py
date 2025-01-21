from flask import Blueprint, render_template

from app import db
from app.models.map import POI, DangerArea, ReliefArea, Coordinates

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
