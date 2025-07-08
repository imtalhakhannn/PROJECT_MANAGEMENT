# Importing the Base and session maker from your FastAPI database config
from app.Database import Base, SessionLocal
from sqlalchemy import Column, Integer, String
# Defining Role Table
class Role(Base):
    __tablename__ = "role"

    # Defining primary key for Role table
    id = Column(Integer, primary_key=True, index=True)

    # Defining unique and non-nullable name field for roles
    name = Column(String(50), unique=True, nullable=False)


# Inserting dummy role data if the file is executed directly
if __name__ == "__main__":
    # Creating a new database session
    db = SessionLocal()

    # Defining list of default roles for insertion
    roles = [
        'CEO', 'Project Manager', 'Project Coordinator', 'Employee', 'Intern',
        'Team Lead', 'QA Engineer', 'Designer', 'HR Manager', 'Data Analyst'
    ]

    # Looping through each role name
    for role_name in roles:
        # Checking if role already exists in the table
        existing = db.query(Role).filter_by(name=role_name).first()

        # Inserting role only if it does not already exist
        if not existing:
            db.add(Role(name=role_name))

    # Committing all changes to the database
    db.commit()

    # Closing the session after use
    db.close()

    print("Roles inserted successfully.")
