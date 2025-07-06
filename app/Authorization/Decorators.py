from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from app.models.User import User

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            #Explicitly verifying the JWT token 
            verify_jwt_in_request()

            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if user is None or user.role.name not in required_roles:
                return jsonify({"msg": "Access denied"}), 403

            return func(user, *args, **kwargs)

        return wrapper
    return decorator
