from flask import Flask, render_template
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import babel, db, get_locale
from app.models.map import Coordinates, POI
from app.reports.routes import bp as reports_bp
from app.volunteers.routes import bp as volunteers_bp
from app.maps.routes import bp as maps_bp

from config import Config


def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(flask_app)
    babel.init_app(flask_app, locale_selector=get_locale)

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        # Tmp do sprawdzenia jak bym zapomniał to usuncie
        coord1 = Coordinates(x=51.74708, y=19.45404)
        coord2 = Coordinates(x=51.74800, y=19.45500)
        db.session.add(coord1)
        db.session.add(coord2)

        poi1 = POI(name="Point A", coordinates=coord1)
        poi2 = POI(name="Point B", coordinates=coord2)
        db.session.add(poi1)
        db.session.add(poi2)

        db.session.commit()

        print("Sample data added successfully!")

    # Register blueprints here
    flask_app.register_blueprint(reports_bp, url_prefix='/reports')

    flask_app.register_blueprint(volunteers_bp, url_prefix='/volunteers')

    flask_app.register_blueprint(maps_bp, url_prefix='/maps')

    @flask_app.route('/')
    def home():
        return render_template('index.jinja')

    @flask_app.route('/db')
    def check_db():
        try:
            with db.engine.connect() as connection:
                result = connection.execute(
                    text('SELECT CURRENT_TIMESTAMP')).scalar()
                print(result)
                if result:
                    return f'Database connection is established. Current timestamp: {result}'
                else:
                    return 'Database connection failed.'
        except SQLAlchemyError as e:
            return f'Database connection failed: {str(e)}'

    return flask_app
