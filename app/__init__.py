from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # config.pyの設定読み込み
    app.config.from_object("config.Config")
    
    # DB接続初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint登録
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from . import models

    return app