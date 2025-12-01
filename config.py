import os
from dotenv import load_dotenv

# .env読み込み
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast" 

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
