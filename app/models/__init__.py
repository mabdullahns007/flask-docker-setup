from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    ID_KEY = "id"
    EMAIL_KEY = "email"
    CREATED_AT_KEY = "created_at"
    LAST_LOGIN_AT_KEY = "last_login_at"

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)


    def __init__(self, email: str, password_hash: str, last_login_at=None):
        self.email = email
        self.password_hash = password_hash

    def to_dict(self):
        return {
            User.ID_KEY: self.id,
            User.EMAIL_KEY: self.email,
            User.CREATED_AT_KEY: (
                self.created_at.isoformat() if self.created_at else None
            ),
            User.LAST_LOGIN_AT_KEY: (
                self.last_login_at.isoformat() if self.last_login_at else None
            ),
        }
