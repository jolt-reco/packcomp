from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name="default"):
    app = Flask(__name__)
    # テスト用app使用する場合
    if config_name == "testing":
        from config import TestingConfig
        app.config.from_object(TestingConfig)
    # 本番用app使用する場合
    else:
        from config import Config
        app.config.from_object(Config)
    
    # DB接続初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint登録
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from . import models

    return app