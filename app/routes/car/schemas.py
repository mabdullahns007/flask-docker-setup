from marshmallow import Schema, fields
from apiflask.fields import String, Integer, List, Nested
from apiflask import PaginationSchema

#Input Schemas
class CarMakeInputSchema(Schema):
    name = String(required=True)

class CarModelInputSchema(Schema):
    name = String(required=True)
    make_id = String()  

class CarYearInputSchema(Schema):
    year = Integer(required=True)
    model_id = String()  

#Output Schemas
class CarMakeOutputSchema(Schema):
    id = String()
    name = String()

class CarModelOutputSchema(Schema):
    id = String()
    name = String()
    make_id = String()

class CarYearOutputSchema(Schema):
    id = String()
    year = Integer()
    model_id = String()

#pagination Schemas
class CarMakeOuts(Schema):
    items = List(Nested(CarMakeOutputSchema))
    pagination = Nested(PaginationSchema)

class CarModelOuts(Schema):
    items = List(Nested(CarModelOutputSchema))
    pagination = Nested(PaginationSchema)

class CarYearOuts(Schema):
    items = List(Nested(CarYearOutputSchema))
    pagination = Nested(PaginationSchema)