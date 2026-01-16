from flask import Blueprint, jsonify, request
from app.models import CarMake, CarModel, CarYear
from app import db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.routes.car.schemas import (car_make_schema,car_model_schema,car_year_schema)
from app.routes.car.decorators import token_required, validate_schema, serialize_response, paginate


car_bp = Blueprint("car", __name__, url_prefix="/cars")

#Car Make APIs

@car_bp.route("/makes", methods=["GET"], strict_slashes=False)
@token_required
@paginate(car_make_schema)
def list_makes(current_user):
    return db.select(CarMake)

@car_bp.route("/makes", methods=["POST"])
@token_required
@validate_schema(car_make_schema)
@serialize_response(car_make_schema)
def create_make(current_user):
    data = request.get_json(silent=True) or {}
    
    make = car_make_schema.load(data)
    db.session.add(make)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Make already exists"}, 409
    
    return make, 201

@car_bp.route("/makes/<string:make_id>", methods=["GET"])
@token_required
@serialize_response(car_make_schema)
def get_make(current_user, make_id):
    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    return make

@car_bp.route("/makes/<string:make_id>", methods=["PUT"])
@token_required
@validate_schema(car_make_schema, partial=True)
@serialize_response(car_make_schema)
def update_make(current_user, make_id):
    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    data = request.get_json(silent=True) or {}
    
    # Marshmallow load with instance updates the existing object
    make = car_make_schema.load(data, instance=make, partial=True)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Make name already exists"}, 409
    return make

@car_bp.route("/makes/<string:make_id>", methods=["DELETE"])
@token_required
def delete_make(current_user, make_id):
    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    db.session.delete(make)
    db.session.commit()
    return jsonify({"message": "Make deleted successfully"}), 200

#Car Model APIs

@car_bp.route("/models", methods=["GET"], strict_slashes=False)
@token_required
@paginate(car_model_schema)
def get_models(current_user):
    return db.select(CarModel)

@car_bp.route("/models", methods=["POST"])
@token_required
@validate_schema(car_model_schema)
@serialize_response(car_model_schema)
def create_model(current_user):
    data = request.get_json(silent=True) or {}
    
    model = car_model_schema.load(data)
    db.session.add(model)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Could not create model"}, 500
    return model, 201

@car_bp.route("/models/<string:model_id>", methods=["GET"])
@token_required
@serialize_response(car_model_schema)
def get_model(current_user, model_id):
    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    return model

@car_bp.route("/models/<string:model_id>", methods=["PUT"])
@token_required
@validate_schema(car_model_schema, partial=True)
@serialize_response(car_model_schema)
def update_model(current_user, model_id):
    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    data = request.get_json(silent=True) or {}
    
    # Marshmallow load with instance updates the existing object
    model = car_model_schema.load(data, instance=model, partial=True)
    
    db.session.commit()
    return model

@car_bp.route("/models/<string:model_id>", methods=["DELETE"])
@token_required
def delete_model(current_user, model_id):
    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    db.session.delete(model)
    db.session.commit()
    return jsonify({"message": "Model deleted successfully"}), 200

#Car Year APIs

@car_bp.route("/years", methods=["GET"], strict_slashes=False)
@token_required
@paginate(car_year_schema)
def get_years(current_user):
    return db.select(CarYear)

@car_bp.route("/years", methods=["POST"])
@token_required
@validate_schema(car_year_schema)
@serialize_response(car_year_schema)
def create_year(current_user):
    data = request.get_json(silent=True) or {}
    
    year = car_year_schema.load(data)
    db.session.add(year)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Year for this model already exists"}, 409
    return year, 201

@car_bp.route("/years/<string:year_id>", methods=["GET"])
@token_required
@serialize_response(car_year_schema)
def get_year(current_user, year_id):
    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    return year

@car_bp.route("/years/<string:year_id>", methods=["PUT"])
@token_required
@validate_schema(car_year_schema, partial=True)
@serialize_response(car_year_schema)
def update_year(current_user, year_id):
    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    data = request.get_json(silent=True) or {}
    
    # Marshmallow load with instance updates the existing object
    year = car_year_schema.load(data, instance=year, partial=True)
    
    db.session.commit()
    return year

@car_bp.route("/years/<string:year_id>", methods=["DELETE"])
@token_required
def delete_year(current_user, year_id):
    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    db.session.delete(year)
    db.session.commit()
    return jsonify({"message": "Year deleted successfully"}), 200

#Error Handler

@car_bp.errorhandler(NotFound)
def handle_not_found(error):
    return jsonify({
        "error": "Resource not found",
        "message": error.description
    }), 404

