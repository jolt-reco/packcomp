import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# .env読み込み
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # config.pyの設定読み込み
    app.config.from_object("config.Config")
    
    # DB接続初期化
    db.init_app(app)

    # Blueprint登録
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app