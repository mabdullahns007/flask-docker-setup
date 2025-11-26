from datetime import datetime, timedelta

import jwt
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _generate_access_token(user: User) -> str:
    issued_at = datetime.utcnow()
    expires_in_minutes = current_app.config.get("JWT_EXPIRATION_MINUTES", 60)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "iat": issued_at,
        "exp": issued_at + timedelta(minutes=expires_in_minutes),
    }

    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400

    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email is already registered."}), 409

    token = _generate_access_token(user)

    return jsonify({"user": user.to_dict(), "token": token}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password."}), 401

    user.last_login_at = datetime.utcnow()

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to complete login at this time."}), 500

    token = _generate_access_token(user)

    return jsonify({"user": user.to_dict(), "token": token}), 200

