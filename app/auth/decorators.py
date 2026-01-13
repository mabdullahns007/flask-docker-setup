from functools import wraps
import jwt
from flask import request, jsonify, current_app
from app.models import User
from app.auth.constants import (JWT_SECRET_KEY_CONFIG_KEY,JWT_ALGORITHM,JWT_SUBJECT_KEY)

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
