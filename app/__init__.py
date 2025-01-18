import os

from flask import Flask, render_template
from flask_mailman import Mail
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config import Config

from app.auth.user_service import init_login_manager
from app.extensions import babel, db, get_locale
from app.reports.routes import bp as reports_bp
from app.volunteers.routes import bp as volunteers_bp
from app.donors.routes import bp as donors_bp
from app.auth.routes import bp as auth_bp

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(flask_app)
    babel.init_app(flask_app, locale_selector=get_locale)

    with flask_app.app_context():
        db.create_all()

    # Initialize login manager
    init_login_manager(flask_app)

    # Initialize flask_mailman
    mail = Mail(flask_app)

    flask_app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    flask_app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
    flask_app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == 'True'
    flask_app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == 'True'
    flask_app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    flask_app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    flask_app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    mail.init_app(flask_app)

    # Register blueprints here
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')

    flask_app.register_blueprint(reports_bp, url_prefix='/reports')

    flask_app.register_blueprint(volunteers_bp, url_prefix='/volunteers')

    flask_app.register_blueprint(donors_bp, url_prefix='/donors')


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
