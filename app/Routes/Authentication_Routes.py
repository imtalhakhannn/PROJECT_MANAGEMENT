# Handles registration and login with JWT authentication

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.User import User
from app.models.Role import Role

auth_bp = Blueprint('auth', __name__)

# Register new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"msg": "Invalid role"}), 400

    hashed_password = generate_password_hash(password)
    user = User(email=email, password=hashed_password, role_id=role.id)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": f"{role_name} registered successfully!"})

#Login to get JWT token
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)  

    return jsonify({
        "access_token": access_token,
        "role": user.role.name,
        "email": user.email
    })
print("auth_bp loaded")
