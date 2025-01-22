import os


class Config:
    SECRET_KEY = 'secret'
    # os.environ.get('SECRET_KEY')

    BABEL_TRANSLATION_DIRECTORIES = '../translations'

    # postgresql+psycopg2://DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    # mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == 'True'
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == 'True'
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
