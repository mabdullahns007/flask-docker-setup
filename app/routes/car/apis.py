from flask import Blueprint, jsonify, request
from app.models import CarMake, CarModel, CarYear
from app import db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.routes.car.schemas import (CarMakeInputSchema,CarModelInputSchema,CarYearInputSchema,CarMakeOutputSchema,CarModelOutputSchema,CarYearOutputSchema, PaginationQuerySchema,genericPaginatedSchema)
from app.routes.car.decorators import token_required, paginationSchema
from apiflask import APIBlueprint


car_bp = APIBlueprint("car", __name__, url_prefix="/cars")

#Car Make APIs
@car_bp.route("/makes", methods=["GET"], strict_slashes=False)
@token_required
@car_bp.input(PaginationQuerySchema, location="query")
@car_bp.output(genericPaginatedSchema(CarMakeOutputSchema))
def list_makes(current_user, query_data):
    page = query_data["page"]
    per_page = query_data["per_page"]
    query = db.session.query(CarMake)
    pagination = query.paginate(page=page, per_page=per_page)
    return paginationSchema(pagination)

@car_bp.route("/makes", methods=["POST"])
@token_required
@car_bp.input(CarMakeInputSchema, location="json")
def create_make(current_user, json_data):
    make = CarMake(name=json_data["name"])
    db.session.add(make)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Make already exists"}, 409
    
    return make.to_dict(), 201

@car_bp.route("/makes/<string:make_id>", methods=["GET"])
@token_required
@car_bp.output(CarMakeOutputSchema)
def get_make(current_user, make_id):
    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    return make, 200

@car_bp.route("/makes/<string:make_id>", methods=["PUT"])
@token_required
@car_bp.input(CarMakeInputSchema, location="json")
def update_make(current_user, make_id, json_data):
    make = db.session.execute(db.select(CarMake).filter_by(id=make_id)).scalar_one_or_none()
    if not make:
        raise NotFound(f"Make with ID {make_id} not found")
    make.name = json_data["name"]
    
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
@car_bp.input(PaginationQuerySchema, location="query")
@car_bp.output(genericPaginatedSchema(CarModelOutputSchema))
def get_models(current_user, query_data):
    page=query_data["page"]
    per_page=query_data["per_page"]
    query=db.session.query(CarModel)
    pagination=query.paginate(page=page, per_page=per_page)
    return paginationSchema(pagination)

@car_bp.route("/models", methods=["POST"])
@token_required
@car_bp.input(CarModelInputSchema, location="json")
def create_model(current_user, json_data):
    model = CarModel(name=json_data["name"], make_id=json_data["make_id"])
    db.session.add(model)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Could not create model"}, 500
    return model.to_dict(), 201

@car_bp.route("/models/<string:model_id>", methods=["GET"])
@token_required
@car_bp.output(CarModelOutputSchema)
def get_model(current_user, model_id):
    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    return model, 200

@car_bp.route("/models/<string:model_id>", methods=["PUT"])
@token_required
@car_bp.input(CarModelInputSchema, location="json")
def update_model(current_user, model_id, json_data):
    model = db.session.execute(db.select(CarModel).filter_by(id=model_id)).scalar_one_or_none()
    if not model:
        raise NotFound(f"Model with ID {model_id} not found")
    model.name = json_data["name"]
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
@car_bp.input(PaginationQuerySchema, location="query")
@car_bp.output(genericPaginatedSchema(CarYearOutputSchema))
def get_years(current_user, query_data):
    page=query_data["page"]
    per_page=query_data["per_page"]
    query=db.session.query(CarYear)
    pagination=query.paginate(page=page, per_page=per_page)
    return paginationSchema(pagination)

@car_bp.route("/years", methods=["POST"])
@token_required
@car_bp.input(CarYearInputSchema, location="json")
def create_year(current_user, json_data):
    year = CarYear(year=json_data["year"], model_id=json_data["model_id"])
    db.session.add(year)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Year for this model already exists"}, 409
    return year.to_dict(), 201

@car_bp.route("/years/<string:year_id>", methods=["GET"])
@token_required
@car_bp.output(CarYearOutputSchema)
def get_year(current_user, year_id):
    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    return year, 200

@car_bp.route("/years/<string:year_id>", methods=["PUT"])
@token_required
@car_bp.input(CarYearInputSchema, location="json")
def update_year(current_user, year_id, json_data):
    year = db.session.execute(db.select(CarYear).filter_by(id=year_id)).scalar_one_or_none()
    if not year:
        raise NotFound(f"Year with ID {year_id} not found")
    year.year = json_data["year"]
    
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

