from datetime import date
from sqlalchemy import Date, Column, Integer, String, ForeignKey
from app.Database import Base, SessionLocal  # Base class and DB session
from sqlalchemy.orm import relationship

# Defining the Task Table 
class Task(Base):
    __tablename__ = "tasks"

    # Creating a primary key column
    id = Column(Integer, primary_key=True, index=True)

    # Defining unique and required task name
    name = Column(String(100), unique=True, nullable=False)

    # Defining task start and end dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    #Defing Rate Column
    Rate=Column(String(500),nullable=False)
    #Defining Quantity Column
    Quantity=Column(Integer,nullable=False)

    # Linking task to a project using foreign key
    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="tasks")
    reports = relationship("Report", back_populates="task")

# Inserting dummy task data when file is run directly
if __name__ == "__main__":
    # Creating a new database session
    db = SessionLocal()

    # Creating a dummy task object
    task = Task(
        name="Planning and Designing",
        start_date=date(2025, 8, 13),
        end_date=date(2025, 10, 20),
        project_id=1
    )

    # Adding the task to the session
    db.add(task)

    # Committing the transaction to the database
    db.commit()

    # Closing the database session
    db.close()

    print(f"The task '{task.name}' is added.")
