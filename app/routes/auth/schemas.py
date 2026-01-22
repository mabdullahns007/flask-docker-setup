from marshmallow import Schema, fields
from apiflask.fields import String, Integer

class UserSchema(Schema):
    email = String(required=True)
    password = String(required=True)
