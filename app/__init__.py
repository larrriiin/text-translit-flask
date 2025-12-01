import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_class: str = "app.config.DevelopmentConfig") -> Flask:
    """Application factory."""
    app = Flask(__name__, instance_relative_config=True)

    # Конфигурация
    app.config.from_object(config_class)

    # Убедимся, что instance и папки для файлов существуют
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["PROCESSED_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    # Регистрация Blueprint'ов или view-модуля
    from app.views import main_bp

    app.register_blueprint(main_bp)

    # Создание БД
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app
