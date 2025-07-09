import random
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.Database import Base, SessionLocal
from app.models.User import User
from app.models.Project import Project


#Creating ProjectUser Table
class ProjectUser(Base):
    __tablename__ = "project_users"


# Creating unique ID for each association
    id = Column(Integer, primary_key=True, index=True)


# Linking to Project table
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)


# Linking to User table
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


# Establishing reverse relationship with Project model
    project = relationship("Project", back_populates="assigned_users")


# Establishing reverse relationship with User model
    user = relationship("User", back_populates="assigned_projects")


# Inserting dummy user-project assignments 
if __name__ == "__main__":

    
# Creating DB session
    db = SessionLocal()


# Fetching all users and projects
    users = db.query(User).all()
    projects = db.query(Project).all()


# Initializing set to track unique user-project pairs
    assigned_pairs = set()


# Generating 10 random unique assignments
    for _ in range(10):
        user = random.choice(users)
        project = random.choice(projects)

        key = (user.id, project.id)
        if key not in assigned_pairs:
# Creating and adding new association
            pu = ProjectUser(user_id=user.id, project_id=project.id)
            db.add(pu)
            assigned_pairs.add(key)  


# Committing changes to DB
    db.commit()
    db.close()
    print("User-project assignments inserted.")
