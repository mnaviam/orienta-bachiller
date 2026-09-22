import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'orientabachiller-super-secret-key-2026'
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'vocacional.db')
    DEBUG = True
    APP_NAME = "OrientaBachiller"
    APP_TAGLINE = "Tu brújula vocacional para elegir tu carrera universitaria con confianza"
