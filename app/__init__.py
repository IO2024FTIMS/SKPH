from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text


from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here

    @app.route('/')
    def hello():
        return "Hello World!!"

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
