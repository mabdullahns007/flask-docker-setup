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
def genericPaginatedSchema(itemSchema):
    class GenericPaginatedSchema(Schema):
        items = List(Nested(itemSchema))
        pagination = Nested(PaginationSchema)
    return GenericPaginatedSchema

# Pagination Query Parameters Schema
class PaginationQuerySchema(Schema):
    page = Integer(load_default=1, metadata={'description': 'Page number'})
    per_page = Integer(load_default=10, metadata={'description': 'Items per page'})
    