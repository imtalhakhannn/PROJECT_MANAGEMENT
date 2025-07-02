#Project Manager creates and assigns users to projects
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from app.models.Projects import Project
from app.models.Projects_User import ProjectUser
from app.models.User import User
from app import db
from app.Authorization.Decorators import role_required

project_bp = Blueprint('project', __name__)

@project_bp.route('/create', methods=['POST'])

@jwt_required()

@role_required(['Project Manager'])  # Only PM can create project

def create_project(current_user):

    print("Current user:", current_user)

    print("Request JSON:", request.get_json())

    data = request.get_json()

    name = data.get('name')
 
    # Validate the 'name' field

    if not isinstance(name, str) or not name.strip():

        return jsonify({"msg": "Project name must be a non-empty string"}), 400
 
    try:

        project = Project(name=name, manager_id=current_user.id)

        db.session.add(project)

        db.session.commit()

        return jsonify({"msg": "Project created successfully", "project_id": project.id}), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({"msg": f"Error creating project: {str(e)}"}), 500
 

@project_bp.route('/assign', methods=['POST'])
@jwt_required()
@role_required(['Project Manager'])  # Only PM can assign users
def assign_user(current_user):
    data = request.get_json()
    project_id = data.get('project_id')
    user_id = data.get('user_id')

    project = Project.query.get(project_id)
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    if project.manager_id != current_user.id:
        return jsonify({"msg": "Unauthorized to assign users"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    existing = ProjectUser.query.filter_by(project_id=project_id, user_id=user_id).first()
    if existing:
        return jsonify({"msg": "User already assigned"}), 400

    assignment = ProjectUser(project_id=project_id, user_id=user_id)
    db.session.add(assignment)
    db.session.commit()

    return jsonify({"msg": "User assigned to project successfully"})
