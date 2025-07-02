#This is a join table to connect Users and  Projects (many-to-many)

from app import db
from app import create_app
import random


class ProjectUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key to Project
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
"""    
if __name__ == "__main__":
 
    app = create_app()
    app.app_context().push()

    users = User.query.all()
    projects = Project.query.all()

    assigned_pairs = set()

    for i in range(10): 
        user = random.choice(users)
        project = random.choice(projects)

        key = (user.id, project.id)
        if key not in assigned_pairs:
            pu = ProjectUser(user_id=user.id, project_id=project.id)
            db.session.add(pu)
            assigned_pairs.add(key)

    db.session.commit()
    print("Dummy user-project assignments inserted.")"""