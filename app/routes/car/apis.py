from flask import Blueprint, jsonify, request
from app.models import CarMake, CarModel, CarYear
from app import db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.routes.car.schemas import (car_make_schema,car_model_schema,car_year_schema)
from app.routes.car.decorators import token_required, validate_schema, paginate


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
def create_make(current_user):
    
    data = request.get_json(silent=True) or {}
    make = CarMake(name=data["name"])
    db.session.add(make)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Make already exists"}, 409
    
    return make.to_dict(), 201

@car_bp.route("/makes/<string:make_id>", methods=["GET"])
@token_required
def get_make(current_user, make_id):

    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    return make.to_dict(), 200

@car_bp.route("/makes/<string:make_id>", methods=["PUT"])
@token_required
@validate_schema(car_make_schema, partial=True)
def update_make(current_user, make_id):

    data = request.get_json(silent=True) or {}
    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    make.name = data["name"]
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Make name already exists"}, 409
    return make.to_dict(), 200

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
def create_model(current_user):

    data = request.get_json(silent=True) or {}
    model = CarModel(name=data["name"], make_id=data["make_id"])
    db.session.add(model)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Could not create model"}, 500
    return model.to_dict(), 201

@car_bp.route("/models/<string:model_id>", methods=["GET"])
@token_required
def get_model(current_user, model_id):

    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    return model.to_dict(), 200

@car_bp.route("/models/<string:model_id>", methods=["PUT"])
@token_required
@validate_schema(car_model_schema, partial=True)
def update_model(current_user, model_id):

    data = request.get_json(silent=True) or {}
    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    model.name = data["name"]
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Model name already exists"}, 409
    return model.to_dict(), 200

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
def create_year(current_user):

    data = request.get_json(silent=True) or {}
    year = CarYear(year=data["year"], model_id=data["model_id"])
    db.session.add(year)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Year for this model already exists"}, 409
    return year.to_dict(), 201

@car_bp.route("/years/<string:year_id>", methods=["GET"])
@token_required
def get_year(current_user, year_id):

    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    return year.to_dict(), 200

@car_bp.route("/years/<string:year_id>", methods=["PUT"])
@token_required
@validate_schema(car_year_schema, partial=True)
def update_year(current_user, year_id):

    data = request.get_json(silent=True) or {}
    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    year.year = data["year"]
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Year for this model already exists"}, 409
    return year.to_dict(), 200

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

