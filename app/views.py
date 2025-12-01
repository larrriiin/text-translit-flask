import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)

from werkzeug.utils import secure_filename

from app import db
from app.models import RequestLog
from app.translit import transliterate

main_bp = Blueprint("main", __name__)


def _allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def _get_client_ip() -> str:
    """Попытка корректно определить IP клиента за прокси."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Берём первый IP из списка
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("Файл не выбран.", "danger")
            return redirect(url_for("main.index"))

        if not _allowed_file(file.filename):
            flash("Разрешены только текстовые файлы (.txt).", "danger")
            return redirect(url_for("main.index"))

        filename = secure_filename(file.filename)
        upload_folder: Path = current_app.config["UPLOAD_FOLDER"]
        processed_folder: Path = current_app.config["PROCESSED_FOLDER"]

        # Сохраняем исходный файл
        upload_path = upload_folder / filename
        file.save(upload_path)

        # Читаем, перекодируем, сохраняем результат
        try:
            with open(upload_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except OSError:
            flash("Ошибка чтения файла на сервере.", "danger")
            return redirect(url_for("main.index"))

        translit_content = transliterate(content)

        name_without_ext, ext = os.path.splitext(filename)
        result_filename = f"{name_without_ext}_translit{ext or '.txt'}"
        result_path = processed_folder / result_filename

        try:
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(translit_content)
        except OSError:
            flash("Ошибка записи файла результата на сервере.", "danger")
            return redirect(url_for("main.index"))

        # Логируем запрос
        log_entry = RequestLog(
            ip_address=_get_client_ip(),
            filename=filename,
        )
        db.session.add(log_entry)
        db.session.commit()

        flash("Файл успешно обработан.", "success")
        return render_template(
            "index.html",
            result_filename=result_filename,
        )

    return render_template("index.html")


@main_bp.route("/download/<path:filename>")
def download_file(filename: str):
    processed_folder: Path = current_app.config["PROCESSED_FOLDER"]
    return send_from_directory(
        processed_folder,
        filename,
        as_attachment=True,
        download_name=filename,
    )


@main_bp.route("/history")
def history():
    logs = RequestLog.query.order_by(RequestLog.created_at.desc()).limit(100).all()
    return render_template("history.html", logs=logs)
