from datetime import datetime, timedelta
import jwt
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db
from app.routes.auth.constants import (EMAIL_PASSWORD_REQUIRED_ERROR,INVALID_EMAIL_FORMAT_ERROR,EMAIL_ALREADY_REGISTERED_ERROR,INVALID_EMAIL_OR_PASSWORD_ERROR,LOGIN_COMPLETION_ERROR,JWT_EXPIRATION_MINUTES_CONFIG_KEY,JWT_SECRET_KEY_CONFIG_KEY,JWT_DEFAULT_EXPIRATION_MINUTES,JWT_ALGORITHM,JWT_SUBJECT_KEY,JWT_EMAIL_KEY,JWT_ISSUED_AT_KEY,JWT_EXPIRATION_KEY,EMAIL_REGEX,PASSWORD_REGEX,PASSWORD_REQUIREMENTS_MESSAGE)
from apiflask import APIBlueprint
from app.routes.auth.schemas import UserSchema

auth_bp = APIBlueprint("auth", __name__, url_prefix="/auth")

def _generate_access_token(user: User) -> str:
    issued_at = datetime.utcnow()
    expires_in_minutes = current_app.config.get(JWT_EXPIRATION_MINUTES_CONFIG_KEY, JWT_DEFAULT_EXPIRATION_MINUTES)
    payload = {
        JWT_SUBJECT_KEY: str(user.id),
        JWT_EMAIL_KEY: user.email,
        JWT_ISSUED_AT_KEY: issued_at,
        JWT_EXPIRATION_KEY: issued_at + timedelta(minutes=expires_in_minutes),
    }
    token = jwt.encode(payload, current_app.config[JWT_SECRET_KEY_CONFIG_KEY], algorithm=JWT_ALGORITHM)
    return token

@auth_bp.route("/signup", methods=["POST"])
@auth_bp.input(UserSchema)
def signup(json_data):
    email = (json_data.get("email") or "").strip().lower()
    password = json_data.get("password")
    if not email or not password:
        return jsonify({"error": EMAIL_PASSWORD_REQUIRED_ERROR}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"error": INVALID_EMAIL_FORMAT_ERROR}), 400

    if not PASSWORD_REGEX.match(password):
        return jsonify({"error": PASSWORD_REQUIREMENTS_MESSAGE}), 400

    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": EMAIL_ALREADY_REGISTERED_ERROR}), 409
    token = _generate_access_token(user)
    return jsonify({"user": user.to_dict(), "token": token}), 201

@auth_bp.route("/login", methods=["POST"])
@auth_bp.input(UserSchema)
def login(json_data):
    email = (json_data.get("email") or "").strip().lower()
    password = json_data.get("password")
    if not email or not password:
        return jsonify({"error": EMAIL_PASSWORD_REQUIRED_ERROR}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"error": INVALID_EMAIL_FORMAT_ERROR}), 400

    user = db.session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": INVALID_EMAIL_OR_PASSWORD_ERROR}), 401
    user.last_login_at = datetime.utcnow()
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": LOGIN_COMPLETION_ERROR}), 500
    token = _generate_access_token(user)
    return jsonify({"user": user.to_dict(), "token": token}), 200
