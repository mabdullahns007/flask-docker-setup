from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint


class CarMake(db.Model):
    __tablename__ = "car_makes"

    # Keys for serialization
    ID_KEY = "id"
    NAME_KEY = "name"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # One-to-many relationship: CarMake has many CarModels
    models = db.relationship("CarModel", back_populates="make", cascade="all, delete-orphan")
    
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            self.ID_KEY: self.id,
            self.NAME_KEY: self.name,
        }

class CarModel(db.Model):
    __tablename__ = "car_models"

    # Keys for serialization
    ID_KEY = "id"
    NAME_KEY = "name"
    MAKE_ID_KEY = "make_id"
    
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

    def to_dict(self):
        return {
            self.ID_KEY: self.id,
            self.NAME_KEY: self.name,
            self.MAKE_ID_KEY: self.make_id,
        }  

class CarYear(db.Model):
    __tablename__ = "car_years"
    
    __table_args__ = (UniqueConstraint("model_id", "year", name="uq_car_year_model_year"),)
    
    # Keys for serialization
    ID_KEY = "id"
    YEAR_KEY = "year"
    MODEL_ID_KEY = "model_id"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("car_models.id"), nullable=False)
    
    # Many-to-one relationship: CarYear belongs to CarModel
    model = db.relationship("CarModel", back_populates="years")
    
    def __init__(self, year: int, model_id: int):
        self.year = year
        self.model_id = model_id

    def to_dict(self):
        return {
            self.ID_KEY: self.id,
            self.YEAR_KEY: self.year,
            self.MODEL_ID_KEY: self.model_id,
        }    
