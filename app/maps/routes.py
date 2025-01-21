from flask import Blueprint, render_template
from app.models.map import POI, DangerArea, ReliefArea

bp = Blueprint('maps', __name__,
               template_folder='../templates/maps',
               static_folder='static',
               static_url_path='maps')

@bp.route('/')
def index():
    pois = POI.query.all()
    danger_areas = DangerArea.query.all()
    relief_areas = ReliefArea.query.all()

    return render_template('map.jinja', pois=pois, danger_areas=danger_areas, relief_areas=relief_areas)
