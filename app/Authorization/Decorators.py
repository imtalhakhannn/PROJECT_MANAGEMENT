from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models import User

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user is None or user.role.name not in required_roles:
                return jsonify({"msg": "Access denied"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
