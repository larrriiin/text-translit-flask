import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "TEST")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{BASE_DIR / 'instance' / 'translit.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Папки для файлов
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    PROCESSED_FOLDER = BASE_DIR / "processed"

    # Максимальный размер загружаемого файла: 2 MB
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # Разрешённые расширения
    ALLOWED_EXTENSIONS = {"txt"}


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
