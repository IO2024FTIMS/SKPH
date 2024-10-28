import os


class Config:
    SECRET_KEY = 'secret'
    # os.environ.get('SECRET_KEY')

    # postgresql+psycopg2://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
