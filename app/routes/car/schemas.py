from marshmallow import Schema, fields

class CarMakeSchema(Schema):
    id = fields.String(dump_only=True)  
    name = fields.String(required=True)

class CarModelSchema(Schema):
    id = fields.String(dump_only=True)  
    name = fields.String(required=True)
    make_id = fields.String(required=True)  

class CarYearSchema(Schema):
    id = fields.String(dump_only=True)  
    year = fields.Integer(required=True)
    model_id = fields.String(required=True)  

car_make_schema = CarMakeSchema()

car_model_schema = CarModelSchema()

car_year_schema = CarYearSchema()
