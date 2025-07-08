from app.Database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Defining the Project Table 
class Project(Base):
    __tablename__ = "project"

    # Primary key ID for each project
    id = Column(Integer, primary_key=True, index=True)

    # Project name 
    name = Column(String(100), nullable=False)

    # Foreign key linking to the user who is the project manager
    manager_id = Column(Integer, ForeignKey("user.id"))

    # Relationship to access the manager's user object from the project
    project_manager = relationship("User", back_populates="managed_projects")

    # Relationship to access the users assigned to a project
    assigned_users = relationship("ProjectUser", back_populates="project")
    # Relationship to access the tasks assigned to a project
    tasks = relationship("Task", back_populates="project")

    # Method to calculate the total number of days for all tasks under this project
    def total_days(self):
        Days = 0
        for task in self.tasks:
            if task.start_date and task.end_date:
                duration = (task.end_date - task.start_date).days
                Days += duration
        return max(Days, 0)  # Ensure duration is not negative

    # Method to return a dictionary representation of the project
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manager_id": self.manager_id,
            "Total_Time": self.total_days()
        }

# Code block to insert dummy data if this file is run directly
if __name__ == "__main__":
    # Import application setup and models
    from app import create_app
    from app.Database import SessionLocal
    from app.models import User, ProjectUser

    # Create a database session
    db_session = SessionLocal()

    # Fetch project manager and employees by their email
    manager_user = db_session.query(User).filter_by(email="pm1@example.com").first()
    employee1 = db_session.query(User).filter_by(email="emp1@example.com").first()
    employee2 = db_session.query(User).filter_by(email="qa1@example.com").first()

    # Only proceed if all required users exist
    if manager_user and employee1 and employee2:

        # Check if a project with the same name already exists
        existing_project = db_session.query(Project).filter_by(name="AI System Upgrade").first()

        if not existing_project:
            # Create new project and assign project manager
            project = Project(name="AI System Upgrade", manager_id=manager_user.id)
            db_session.add(project)
            db_session.commit()

            # Assign employees to the project
            assignment1 = ProjectUser(project_id=project.id, user_id=employee1.id)
            assignment2 = ProjectUser(project_id=project.id, user_id=employee2.id)

            # Add assignments to the database
            db_session.add_all([assignment1, assignment2])
            db_session.commit()

            print("Dummy project and user assignments inserted successfully.")
        else:
            print("Project already exists.")
    else:
        print("Required users not found. Please insert dummy users first.")
