# Importing required modules and functions
# Importing password hashing utility
from werkzeug.security import generate_password_hash
# Importing the database instance
from app import db
# Importing Role model for foreign key relationships
from app.models.Role import Role
# Defining the User model for storing user-related data
# Users can manage or be assigned to projects
class User(db.Model):
    # Defining primary key column
    id = db.Column(db.Integer, primary_key=True)
    # Defining unique and required email column
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Storing hashed password securely
    password = db.Column(db.String(600), nullable=False)
    # Creating relationship with Role model (one-to-many)
    role = db.relationship('Role', backref='users')
    # Defining foreign key for user's role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    # Creating relationship for projects managed by this user
    managed_projects = db.relationship('Project', backref='manager', lazy=True)
    # Creating relationship for projects this user is assigned to
    assigned_projects = db.relationship('ProjectUser', backref='user', lazy=True)

# Running the dummy data insertion when this file is executed directly
if __name__ == "__main__":
    # Importing the app factory
    from app import create_app

    # Creating and pushing application context
    app = create_app()
    app.app_context().push()

    # Defining a list of dummy users with emails and roles
    dummy_users = [
        {"email": "ceo1@example.com", "role": "CEO"},
        {"email": "pm1@example.com", "role": "Project Manager"},
        {"email": "pc1@example.com", "role": "Project Coordinator"},
        {"email": "emp1@example.com", "role": "Employee"},
        {"email": "intern1@example.com", "role": "Employee"},
        {"email": "lead1@example.com", "role": "Project Manager"},
        {"email": "qa1@example.com", "role": "Employee"},
        {"email": "design1@example.com", "role": "Employee"},
        {"email": "hr1@example.com", "role": "HR Manager"},
        {"email": "analyst1@example.com", "role": "Project Coordinator"},
        {"email": "hr2@example.com", "role": "HR Manager"},
        {"email": "pm3@example.com", "role": "Project Manager"},
        {"email": "pm4@example.com", "role": "Project Manager"}
    ]

    # Iterating over dummy user data
    for u in dummy_users:
        # Checking if the user already exists
        existing_user = User.query.filter_by(email=u["email"]).first()
        # Fetching role object by name
        role = Role.query.filter_by(name=u["role"]).first()

        # Creating and adding the user if not already present
        if not existing_user and role:
            user = User(
                email=u["email"],
                password=generate_password_hash("password123"),  # Hashing the password
                role_id=role.id
            )
            db.session.add(user)

    # Committing all new users to the database
    db.session.commit()
    # Printing confirmation message
    print(" Dummy users inserted successfully.")
