#CEO uses this to create other users like Project Managers

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.User import User
from app.models.Role import Role
from app import db
from app.Authorization.Decorators import role_required
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/create-user', methods=['POST'])
@jwt_required()
@role_required(['CEO']) 
# Only CEO allowed
def create_user(current_user):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"msg": "Invalid role"}), 400

    hashed = generate_password_hash(password)
    new_user = User(email=email, password=hashed, role_id=role.id)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": f"{role_name} created successfully by CEO!"})
__all__ = ['user_bp']
