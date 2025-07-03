from app import db

# Project model that represents a project in the system
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each project
    name = db.Column(db.String(120), nullable=False)  # Project name (cannot be null)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to the manager (User)
    assigned_users = db.relationship('ProjectUser', backref='project', lazy=True)  # Relationship to assigned users via ProjectUser table
   
    def to_dict(self):
       
       return {
        "id": self.id,
        "name": self.name,
        "manager_id": self.manager_id
    }


# Section to insert dummy data
if __name__ == "__main__":
    # Import the function to create the Flask app
    from app import create_app  
    # Import related models
    from app.models import User, ProjectUser  

    app = create_app()
    # Activate Flask application context# Activate Flask application context

    manager_user = User.query.filter_by(email="pm1@example.com").first()
    employee1 = User.query.filter_by(email="emp1@example.com").first()
    employee2 = User.query.filter_by(email="qa1@example.com").first()

    # Proceed only if all required users are found
    if manager_user and employee1 and employee2:

        # Check if the project already exists to avoid duplicate insertion
        existing_project = Project.query.filter_by(name="AI System Upgrade").first()
        if not existing_project:
            # Create a new project and assign the manager
            project = Project(
                name="AI System Upgrade",
                manager_id=manager_user.id
            )
            db.session.add(project)
            # Saving the new project to the database
            db.session.commit()  # Saving the new project to the database

            # Assigning users to the project via the ProjectUser association table
            assignment1 = ProjectUser(project_id=project.id, user_id=employee1.id)
            assignment2 = ProjectUser(project_id=project.id, user_id=employee2.id)

            db.session.add_all([assignment1, assignment2])
            db.session.commit()  
            print("Dummy project and user assignments inserted successfully.")
        else:
            print("Project already exists.")
    else:
        print("Required users not found. Please insert dummy users first.")
