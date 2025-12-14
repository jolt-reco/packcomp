from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

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
    login_manager.init_app(app)

    # CSRF対策初期化
    csrf.init_app(app)

    # Blueprint登録
    from app.main import main_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # 未ログインユーザーをログインページへリダイレクト
    login_manager.login_view = "auth.login"

    from . import models

    return app

from app import db
from app.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))