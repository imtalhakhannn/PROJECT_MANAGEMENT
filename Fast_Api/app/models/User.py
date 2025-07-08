from werkzeug.security import generate_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.Database import Base, SessionLocal
from app.models.Role import Role

# Defining the User Table 
class User(Base):
    __tablename__ = "user"

    # Creating unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)

    # Storing user's email 
    email = Column(String(120), unique=True, nullable=False)

    # Storing hashed password
    password = Column(String(600), nullable=False)

    # Linking user to a role using foreign key
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

    # Establishing relationship with Role 
    role = relationship('Role', backref='users')

    # Establishing relationship with projects user manages
    managed_projects = relationship("Project", back_populates="project_manager")


    # Establishing relationship with projects assigned to user
    assigned_projects = relationship("ProjectUser", back_populates="user")
    reports = relationship("Report", back_populates="user")


# Inserting dummy users when file is run directly
if __name__ == "__main__":
    # Creating a new DB session
    db = SessionLocal()

    # Defining dummy user data with email and role name
    dummy_users = [
        {"email": "ceo1@example.com", "role": "CEO"},
        {"email": "pm1@example.com", "role": "Project Manager"},
        {"email": "team_134@example.com", "role": "Team Lead"},
        {"email": "emp1@example.com", "role": "Employee"},
        {"email": "emp2@example.com", "role": "Employee"},
        {"email": "emp3@example.com", "role": "Employee"},
        {"email": "emp4@example.com", "role": "Employee"},
        {"email": "emp5@example.com", "role": "Employee"},
        {"email": "emp6@example.com", "role": "Employee"},
        {"email": "emp7@example.com", "role": "Employee"},
        {"email": "emp8@example.com", "role": "Employee"},
        {"email": "emp9@example.com", "role": "Employee"},
        {"email": "hr@example.com", "role": "HR Manager"},
        {"email": "Qa_134@example.com", "role": "QA Tester"},
        {"email": "Dev_349@example.com", "role": "Developer"},
    ]

    # Iterating through dummy users
    for u in dummy_users:
        # Checking if user already exists
        existing_user = db.query(User).filter_by(email=u["email"]).first()

        # Fetching role by name
        role = db.query(Role).filter_by(name=u["role"]).first()

        # Adding new user if not exists and role is valid
        if not existing_user and role:
            user = User(
                email=u["email"],
                password=generate_password_hash("password123"),
                role_id=role.id
            )
            db.add(user)

    # Saving all users to the DB
    db.commit()
    db.close()

    print("Users inserted successfully.")
