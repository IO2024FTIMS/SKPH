__author__ = "Maciej Kowalski, Mateusz Luzak"

from flask import Flask


def create_app():
    app = Flask(__name__)
    # narazie bez inicjalizacji bazy danych

    #from app.reports.routes import reports_bp
    #app.register_blueprint(reports_bp, url_prefix='/reports')

    return app
