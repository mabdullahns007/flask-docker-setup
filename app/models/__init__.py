from datetime import datetime
from app import db
class User(db.Model):

    # Keys for serialization
    ID_KEY = "id"
    EMAIL_KEY = "email"
    PASSWORD_HASH_KEY = "password_hash"
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
        self.last_login_at = last_login_at
    def to_dict(self):
        return {
            self.ID_KEY: self.id,
            self.EMAIL_KEY: self.email,
            self.PASSWORD_HASH_KEY: self.password_hash,
            self.CREATED_AT_KEY: (
                self.created_at.isoformat() if self.created_at else None
            ),
            self.LAST_LOGIN_AT_KEY: (
                self.last_login_at.isoformat() if self.last_login_at else None
            ),
        }
