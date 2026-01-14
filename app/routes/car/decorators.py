from functools import wraps
import jwt
from flask import request, jsonify, current_app
from app.models import User
from app.routes.auth.constants import (JWT_SECRET_KEY_CONFIG_KEY,JWT_ALGORITHM,JWT_SUBJECT_KEY)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if Authorization header is present
        auth_header = request.headers.get("Authorization")
        print(auth_header)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            elif len(parts) == 1:
                # Fallback: maybe they just sent the token directly
                token = parts[0]
        
        # Fallback to query parameter if still no token
        if not token:
            token = request.args.get('token')

        if not token:
            return jsonify({"error": "Authentication token is missing"}), 401

        try:
            # Decode the token
            payload = jwt.decode(
                token, 
                current_app.config[JWT_SECRET_KEY_CONFIG_KEY], 
                algorithms=[JWT_ALGORITHM]
            )
            # Get the user ID from the token subject
            user_id = payload[JWT_SUBJECT_KEY]
            current_user = User.query.get(user_id)
            if not current_user:
                return jsonify({"error": "Invalid authentication token"}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Authentication token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authentication token"}), 401
        except Exception:
            return jsonify({"error": "Authentication failed"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def validate_schema(schema, partial=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            errors = schema.validate(data, partial=partial)
            if errors:
                return jsonify(errors), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def serialize_response(schema, many=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            
            # Check if result is a tuple (data, status_code)
            if isinstance(result, tuple) and len(result) == 2:
                data, status_code = result
            else:
                data = result
                status_code = 200
            
            # Serialize the data using the provided schema
            serialized_data = schema.dump(data)
            return jsonify(serialized_data), status_code
        return decorated_function
    return decorator

def paginate(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get pagination parameters from query string
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            
            # Limit per_page to prevent abuse
            per_page = min(per_page, 100)
            
            # Call the route function - it should return a query object
            query = f(*args, **kwargs)
            
            # Paginate the query
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            # Serialize the items
            serialized_items = schema.dump(pagination.items, many=True)
            
            # Build response
            response = {
                'items': serialized_items,
                'pagination': {
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'current_page': pagination.page,
                    'per_page': pagination.per_page,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
            return jsonify(response), 200
            
        return decorated_function
    return decorator
