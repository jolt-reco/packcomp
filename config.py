import os
from dotenv import load_dotenv

# .env読み込み
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    NOMINATIM_URI = ("https://nominatim.openstreetmap.org/search")
    OPENMETEO_URI = ("https://api.open-meteo.com/v1/forecast")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
