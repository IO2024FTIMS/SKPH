import json

from flask import Flask, render_template
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import babel, db, get_locale
from app.models.map import Coordinates, POI, DangerArea, ReliefArea
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
