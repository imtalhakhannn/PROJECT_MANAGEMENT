# This model defines a project, managed by a Project Manager
from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # Foreign key to manager (User table)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # List of assigned users (via project_user join table)
 
    assigned_users = db.relationship('ProjectUser', backref='project', lazy=True)
"""
if __name__ == "__main__":
    
    app = create_app()
    app.app_context().push()

    # Pick first 3 project managers to assign
    managers = User.query.join(User.role).filter_by(name="Project Manager").limit(3).all()

    dummy_projects = [
        "Inventory System",
        "HR Portal",
        "E-commerce Site",
        "Mobile App Tracker",
        "Finance Dashboard",
        "Task Manager",
        "CRM Tool",
        "Learning Platform",
        "Visitor Log",
        "Freelance Hub"
    ]

    for i, proj_name in enumerate(dummy_projects):
        manager = managers[i % len(managers)]
        existing = Project.query.filter_by(name=proj_name).first()
        if not existing:
            p = Project(name=proj_name, manager_id=manager.id)
            db.session.add(p)

    db.session.commit()
    print("Dummy projects inserted.")"""