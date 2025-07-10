from werkzeug.security import generate_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.Database import Base, SessionLocal
from app.models.Role import Role


# Defining the User table 
class User(Base):
    __tablename__ = "user"


# Defining primary key for the user
    id = Column(Integer, primary_key=True, index=True)
    

# Storing user's email with unique constraint
    email = Column(String(120), unique=True, nullable=False)
    

# Storing hashed password
    password = Column(String(600), nullable=False)
    

# Linking user to their role via foreign key
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)


#Adding reports created by field to connect with the user
    created_by=Column(String(255),nullable=False)


# CReating user names field
    user_name=Column(String(255),nullable=False)


# Establishing relationship with Role model
    role = relationship('Role', backref='users')
    

# Defining projects this user manages
    managed_projects = relationship("Project", back_populates="project_manager")
    

# Defining projects assigned to this user
    assigned_projects = relationship("ProjectUser", back_populates="user")
    

# Defining reports submitted by this user
    reports = relationship("Report", back_populates="user")
    

# Tracking the user who created this user (if applicable)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=True)
    

# Establishing relationship to the creator (self-referencing)
    creator = relationship("User", remote_side='User.id')


# Linking user to their assigned tasks
    user_tasks = relationship("UserTask", back_populates="user")


# Inserting dummy users when file is run directly
if __name__ == "__main__":


# Creating a new DB session
    db = SessionLocal()
    ceo = db.query(User).filter_by(email="ceo1@example.com").first()
    pm=db.query(User).filter_by(email="pm1@example.com").first()
    hr=db.query(User).filter_by(email="hr@example.com").first()


# Defining dummy user data with email and role name
    dummy_users = [
        {"email": "ceo1@example.com", "role": "CEO","created_by": ceo.id},
        {"email": "pm1@example.com", "role": "Project Manager","created_by": ceo.id},
        {"email": "team_134@example.com", "role": "Team Lead","created_by": ceo.id},
        {"email": "emp1@example.com", "role": "Employee","created_by": ceo.id},
        {"email": "emp2@example.com", "role": "Employee","created_by": ceo.id},
        {"email": "emp3@example.com", "role": "Employee","created_by": ceo.id},
        {"email": "emp4@example.com", "role": "Employee","created_by": ceo.id},
        {"email": "emp5@example.com", "role": "Employee","created_by": pm.id},
        {"email": "emp6@example.com", "role": "Employee","created_by": pm.id},
        {"email": "emp7@example.com", "role": "Employee","created_by": pm.id},
        {"email": "emp8@example.com", "role": "Employee","created_by": pm.id},
        {"email": "emp9@example.com", "role": "Employee","created_by": hr.id},
        {"email": "emp10@example.com", "role": "Employee","created_by": hr.id},
        {"email": "emp11@example.com", "role": "Employee","created_by": hr.id},
        {"email": "emp12@example.com", "role": "Employee","created_by": hr.id},
        {"email": "emp13@example.com", "role": "Employee","created_by": hr.id},
        {"email": "hr@example.com", "role": "HR Manager","created_by": ceo.id},
        {"email": "Qa_134@example.com", "role": "QA Tester","created_by": ceo.id},
        {"email": "Dev_349@example.com", "role": "Developer","created_by": ceo.id},
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
                role_id=role.id,
                created_by=u.get("created_by")
            )
            db.add(user)


# Saving all users to the DB
    db.commit()
    db.close()
    print("Users inserted successfully.")
