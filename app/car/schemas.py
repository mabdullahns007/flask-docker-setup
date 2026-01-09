from app import ma
from app.models import CarMake, CarModel, CarYear
from marshmallow import fields

class CarMakeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarMake
        load_instance = True  # Optional: deseralize to model instances

class CarModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarModel
        load_instance = True
        include_fk = True

class CarYearSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarYear
        load_instance = True
        include_fk = True

# Initialize schemas
car_make_schema = CarMakeSchema()
car_makes_schema = CarMakeSchema(many=True)

car_model_schema = CarModelSchema()
car_models_schema = CarModelSchema(many=True)

car_year_schema = CarYearSchema()
car_years_schema = CarYearSchema(many=True)
