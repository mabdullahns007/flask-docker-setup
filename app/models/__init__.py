from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint


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


class CarMake(db.Model):
    __tablename__ = "car_makes"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # One-to-many relationship: CarMake has many CarModels
    models = db.relationship("CarModel", back_populates="make", cascade="all, delete-orphan")
    
    def __init__(self, name: str):
        self.name = name


class CarModel(db.Model):
    __tablename__ = "car_models"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey("car_makes.id"), nullable=False)
    
    # Many-to-one relationship: CarModel belongs to CarMake
    make = db.relationship("CarMake", back_populates="models")
    
    # One-to-many relationship: CarModel has many CarYears
    years = db.relationship("CarYear", back_populates="model", cascade="all, delete-orphan")
    
    def __init__(self, name: str, make_id: int):
        self.name = name
        self.make_id = make_id


class CarYear(db.Model):
    __tablename__ = "car_years"
    
    __table_args__ = (UniqueConstraint("model_id", "year", name="uq_car_year_model_year"),)
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("car_models.id"), nullable=False)
    
    # Many-to-one relationship: CarYear belongs to CarModel
    model = db.relationship("CarModel", back_populates="years")
    
    def __init__(self, year: int, model_id: int):
        self.year = year
        self.model_id = model_id
