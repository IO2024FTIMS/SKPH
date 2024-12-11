from flask import Flask, render_template
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

import app.models
from app.extensions import babel, db, get_locale
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    with app.app_context():
        db.drop_all()
        db.create_all()

    # Register blueprints here
    from app.volunteers.routes import bp as volunteers_bp
    app.register_blueprint(volunteers_bp, url_prefix='/volunteers')

    @app.route('/')
    def home():
        return render_template('index.jinja')

    @app.route('/db')
    def check_db():
        try:
            with db.engine.connect() as connection:
                result = connection.execute(
                    text("SELECT CURRENT_TIMESTAMP")).scalar()
                print(result)
                if result:
                    return f"Database connection is established. Current timestamp: {result}"
                else:
                    return "Database connection failed."
        except SQLAlchemyError as e:
            return f"Database connection failed: {str(e)}"

    return app
