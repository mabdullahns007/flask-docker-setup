from flask import Blueprint, jsonify, request
from app.models import CarMake, CarModel, CarYear
from app import db, ma
from sqlalchemy.exc import IntegrityError
from app.schemas.car import car_make_schema, car_makes_schema


car_bp = Blueprint("car", __name__, url_prefix="/cars")

@car_bp.route("/makes", methods=["GET"])
def list_makes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = CarMake.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [make.to_dict() for make in pagination.items],
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
    
    name = data.get("name")
    make = CarMake(name=name)
    db.session.add(make)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Make already exists"}), 409
    
    return car_make_schema.jsonify(make), 201

@car_bp.route("/makes/<int:make_id>", methods=["GET"])
def get_make(make_id):
    make = CarMake.query.get_or_404(make_id)
    return jsonify(make.to_dict()), 200

@car_bp.route("/makes/<int:make_id>", methods=["PUT"])
def update_make(make_id):
    make = CarMake.query.get_or_404(make_id)
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if name:
        make.name = name
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Make name already exists"}), 409
    return jsonify(make.to_dict()), 200

@car_bp.route("/makes/<int:make_id>", methods=["DELETE"])
def delete_make(make_id):
    make = CarMake.query.get_or_404(make_id)
    db.session.delete(make)
    db.session.commit()
    return jsonify({"message": "Make deleted successfully"}), 200

# --- CarModel CRUD ---

@car_bp.route("/models", methods=["GET"])
def get_models():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = CarModel.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [model.to_dict() for model in pagination.items],
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
    name = data.get("name")
    make_id = data.get("make_id")
    if not name or not make_id:
        return jsonify({"error": "Name and make_id are required"}), 400
    
    model = CarModel(name=name, make_id=make_id)
    db.session.add(model)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create model"}), 500
    return jsonify(model.to_dict()), 201

@car_bp.route("/models/<int:model_id>", methods=["GET"])
def get_model(model_id):
    model = CarModel.query.get_or_404(model_id)
    return jsonify(model.to_dict()), 200

@car_bp.route("/models/<int:model_id>", methods=["PUT"])
def update_model(model_id):
    model = CarModel.query.get_or_404(model_id)
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    make_id = data.get("make_id")
    if name:
        model.name = name
    if make_id:
        model.make_id = make_id
    db.session.commit()
    return jsonify(model.to_dict()), 200

@car_bp.route("/models/<int:model_id>", methods=["DELETE"])
def delete_model(model_id):
    model = CarModel.query.get_or_404(model_id)
    db.session.delete(model)
    db.session.commit()
    return jsonify({"message": "Model deleted successfully"}), 200

# --- CarYear CRUD ---

@car_bp.route("/years", methods=["GET"])
def get_years():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = CarYear.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [year.to_dict() for year in pagination.items],
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
    year_val = data.get("year")
    model_id = data.get("model_id")
    if not year_val or not model_id:
        return jsonify({"error": "Year and model_id are required"}), 400
    
    year = CarYear(year=year_val, model_id=model_id)
    db.session.add(year)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Year for this model already exists"}), 409
    return jsonify(year.to_dict()), 201

@car_bp.route("/years/<int:year_id>", methods=["GET"])
def get_year(year_id):
    year = CarYear.query.get_or_404(year_id)
    return jsonify(year.to_dict()), 200

@car_bp.route("/years/<int:year_id>", methods=["PUT"])
def update_year(year_id):
    year = CarYear.query.get_or_404(year_id)
    data = request.get_json(silent=True) or {}
    year_val = data.get("year")
    model_id = data.get("model_id")
    if year_val:
        year.year = year_val
    if model_id:
        year.model_id = model_id
    db.session.commit()
    return jsonify(year.to_dict()), 200

@car_bp.route("/years/<int:year_id>", methods=["DELETE"])
def delete_year(year_id):
    year = CarYear.query.get_or_404(year_id)
    db.session.delete(year)
    db.session.commit()
    return jsonify({"message": "Year deleted successfully"}), 200
