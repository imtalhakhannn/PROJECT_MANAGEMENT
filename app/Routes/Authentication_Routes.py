# Creating a blueprint for authentication-related routes
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.User import User
from app.models.Role import Role

# Defining the auth blueprint
auth_bp = Blueprint('auth', __name__)

# Handling registration of a new user
@auth_bp.route('/Signup', methods=['POST'])
def register():
    # Getting JSON data from the request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    # Checking if user with the given email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    # Fetching the role by name
    role = Role.query.filter_by(name=role_name).first()
    # Returning error if the role does not exist
    if not role:
        return jsonify({"msg": "Invalid role"}), 400

    # Hashing the user's password before saving
    hashed_password = generate_password_hash(password)
    # Creating a new User object
    user = User(email=email, password=hashed_password, role_id=role.id)

    # Adding the user to the database session and committing
    db.session.add(user)
    db.session.commit()

    # Returning success message
    return jsonify({"msg": f"{role_name} registered successfully!"})

# Handling login and JWT token generation
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
 
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401
   
 
    # Convert user.id to string for JWT identity
    access_token = create_access_token(identity=str(user.id))
 
    return jsonify({
        "access_token": access_token,
        "role": user.role.name,
        "email": user.email
    }), 200
 
print("auth_bp loaded")

@auth_bp.route('/create-role', methods=['POST'])
def create_role():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"msg": "Role name required"}), 400

    if Role.query.filter_by(name=name).first():
        return jsonify({"msg": "Role already exists"}), 400

    new_role = Role(name=name)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({"msg": f"Role '{name}' created successfully"}), 201
