# Users can manage or be assigned to projects
from werkzeug.security import generate_password_hash
from app import db
from app.models.Role import Role


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)
    role = db.relationship('Role', backref='users')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    managed_projects = db.relationship('Project', backref='manager', lazy=True)
    assigned_projects = db.relationship('ProjectUser', backref='user', lazy=True)

  
if __name__ == "__main__":
    from app import create_app

    app = create_app()
    app.app_context().push()

    dummy_users = [
        {"email": "ceo1@example.com", "role": "CEO"},
        {"email": "pm1@example.com", "role": "Project Manager"},
        {"email": "pc1@example.com", "role": "Project Coordinator"},
        {"email": "emp1@example.com", "role": "Employee"},
        {"email": "intern1@example.com", "role": "Employee"},
        {"email": "lead1@example.com", "role": "Project Manager"},
        {"email": "qa1@example.com", "role": "Employee"},
        {"email": "design1@example.com", "role": "Employee"},
        {"email": "hr1@example.com", "role": "CEO"},
        {"email": "analyst1@example.com", "role": "Project Coordinator"},
    ]

    for u in dummy_users:
        existing_user = User.query.filter_by(email=u["email"]).first()
        role = Role.query.filter_by(name=u["role"]).first()

        if not existing_user and role:
            user = User(
                email=u["email"],
                password=generate_password_hash("password123"),
                role_id=role.id
            )
            db.session.add(user)

    db.session.commit()
    print(" Dummy users inserted successfully.")
