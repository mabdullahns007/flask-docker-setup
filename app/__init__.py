import os

from dotenv import load_dotenv
from flask import Flask

from app.models import db


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", app.config["SECRET_KEY"])

    try:
        expiration_minutes = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))
    except ValueError:
        expiration_minutes = 60

    app.config["JWT_EXPIRATION_MINUTES"] = expiration_minutes

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.ping import ping_bp

    app.register_blueprint(ping_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app

