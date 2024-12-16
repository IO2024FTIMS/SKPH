from flask import request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_locale():
    language = request.accept_languages.best_match(['en', 'pl'])
    return language


db = SQLAlchemy(model_class=Base)
babel = Babel()
