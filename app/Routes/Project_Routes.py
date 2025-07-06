#Project Manager creates and assigns users to projects
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from flask import Blueprint, request, jsonify
from app.models.Projects import Project
from app.models.Projects_User import ProjectUser
from app.models.User import User
from app import db
from app.Authorization.Decorators import role_required
from datetime import datetime
from app.models.Task import Task

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
# Only PM can assign users
@role_required(['Project Manager'])  
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


@project_bp.route('/project_created', methods=['GET'])
@jwt_required()
def get_pm_created_projects():
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)

        if not current_user:
            return jsonify({"msg": "User not found"}), 404

        created_projects = Project.query.filter_by(manager_id=current_user.id).all()

        project_list = [project.to_dict() for project in created_projects]
        return jsonify(project_list), 200

    except Exception as e:
        return jsonify({"msg": f"Error fetching created projects: {str(e)}"}), 500




@project_bp.route('/<int:project_id>/tasks', methods=['POST'])
@jwt_required()
@role_required(['Project Manager']) 
def add_tasks_to_project(current_user, project_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"msg": "Project not found"}), 404

        if project.manager_id != current_user.id:
            return jsonify({"msg": "Unauthorized"}), 403

        data = request.get_json()
        tasks = data.get('tasks', [])

        if not isinstance(tasks, list) or not tasks:
            return jsonify({"msg": "Tasks must be a non-empty list"}), 400

        for task_data in tasks:
            name = task_data.get('name')
            start_date = task_data.get('start_date')
            end_date = task_data.get('end_date')

            # Validate fields
            if not all([name, start_date, end_date]):
                return jsonify({"msg": "Each task must have name, start_date, and end_date"}), 400

            # Convert date strings to Date objects
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"msg": "Date must be in YYYY-MM-DD format"}), 400

            # Create task
            task = Task(
                name=name,
                start_date=start_date,
                end_date=end_date,
                project_id=project_id
            )
            db.session.add(task)

        db.session.commit()
        return jsonify({"msg": f"{len(tasks)} task(s) added to project"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error adding tasks: {str(e)}"}), 500
