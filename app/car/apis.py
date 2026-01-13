from flask import Blueprint, jsonify, request
from app.models import CarMake, CarModel, CarYear
from app import db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.car.schemas import (car_make_schema, car_makes_schema,car_model_schema, car_models_schema,car_year_schema, car_years_schema)


car_bp = Blueprint("car", __name__, url_prefix="/cars")

@car_bp.route("/makes", methods=["GET"], strict_slashes=False)
def list_makes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = CarMake.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": car_makes_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200

@car_bp.route("/makes", methods=["POST"])
def create_make():
    data = request.get_json(silent=True) or {}
    
    # Use Marshmallow to load and validate data
    errors = car_make_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    make = car_make_schema.load(data)
    db.session.add(make)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Make already exists"}), 409
    
    return car_make_schema.jsonify(make), 201

@car_bp.route("/makes/<string:make_id>", methods=["GET"])
def get_make(make_id):
    make = CarMake.query.get_or_404(make_id)
    return car_make_schema.jsonify(make), 200

@car_bp.route("/makes/<string:make_id>", methods=["PUT"])
def update_make(make_id):
    make = CarMake.query.get_or_404(make_id)
    data = request.get_json(silent=True) or {}
    
    # Use Marshmallow to load and validate data (partial=True for updates)
    errors = car_make_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    # Marshmallow load with instance updates the existing object
    make = car_make_schema.load(data, instance=make, partial=True)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Make name already exists"}), 409
    return car_make_schema.jsonify(make), 200

@car_bp.route("/makes/<string:make_id>", methods=["DELETE"])
def delete_make(make_id):
    make = CarMake.query.get_or_404(make_id)
    db.session.delete(make)
    db.session.commit()
    return jsonify({"message": "Make deleted successfully"}), 200

@car_bp.route("/models", methods=["GET"], strict_slashes=False)
def get_models():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = CarModel.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": car_models_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200

@car_bp.route("/models", methods=["POST"])
def create_model():
    data = request.get_json(silent=True) or {}
    
    # Use Marshmallow to load and validate data
    errors = car_model_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    model = car_model_schema.load(data)
    db.session.add(model)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create model"}), 500
    return car_model_schema.jsonify(model), 201

@car_bp.route("/models/<string:model_id>", methods=["GET"])
def get_model(model_id):
    model = CarModel.query.get_or_404(model_id)
    return car_model_schema.jsonify(model), 200

@car_bp.route("/models/<string:model_id>", methods=["PUT"])
def update_model(model_id):
    model = CarModel.query.get_or_404(model_id)
    data = request.get_json(silent=True) or {}
    
    # Use Marshmallow to load and validate data (partial=True for updates)
    errors = car_model_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    # Marshmallow load with instance updates the existing object
    model = car_model_schema.load(data, instance=model, partial=True)
    
    db.session.commit()
    return car_model_schema.jsonify(model), 200

@car_bp.route("/models/<string:model_id>", methods=["DELETE"])
def delete_model(model_id):
    model = CarModel.query.get_or_404(model_id)
    db.session.delete(model)
    db.session.commit()
    return jsonify({"message": "Model deleted successfully"}), 200

# --- CarYear CRUD ---

@car_bp.route("/years", methods=["GET"], strict_slashes=False)
def get_years():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = CarYear.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": car_years_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200

@car_bp.route("/years", methods=["POST"])
def create_year():
    data = request.get_json(silent=True) or {}
    
    # Use Marshmallow to load and validate data
    errors = car_year_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    year = car_year_schema.load(data)
    db.session.add(year)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Year for this model already exists"}), 409
    return car_year_schema.jsonify(year), 201

@car_bp.route("/years/<string:year_id>", methods=["GET"])
def get_year(year_id):
    year = CarYear.query.get_or_404(year_id)
    return car_year_schema.jsonify(year), 200

@car_bp.route("/years/<string:year_id>", methods=["PUT"])
def update_year(year_id):
    year = CarYear.query.get_or_404(year_id)
    data = request.get_json(silent=True) or {}
    
    # Use Marshmallow to load and validate data (partial=True for updates)
    errors = car_year_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    # Marshmallow load with instance updates the existing object
    year = car_year_schema.load(data, instance=year, partial=True)
    
    db.session.commit()
    return car_year_schema.jsonify(year), 200

@car_bp.route("/years/<string:year_id>", methods=["DELETE"])
def delete_year(year_id):
    year = CarYear.query.get_or_404(year_id)
    db.session.delete(year)
    db.session.commit()
    return jsonify({"message": "Year deleted successfully"}), 200

@car_bp.errorhandler(NotFound)
def handle_not_found(error):
    return jsonify({
        "error": "Resource not found",
        "message": error.description
    }), 404

