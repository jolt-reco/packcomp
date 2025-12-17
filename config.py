import os
from dotenv import load_dotenv

# .env読み込み
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///packcomp.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    OPENMETEO_URI = ("https://api.open-meteo.com/v1/forecast")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
