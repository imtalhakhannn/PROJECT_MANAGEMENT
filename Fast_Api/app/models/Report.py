from __future__ import annotations
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime,String,Float
from sqlalchemy.orm import relationship
from app.models import Task, User
from app.Database import Base, SessionLocal
from app.models import User


# Defining the Report Table
class Report(Base):
    __tablename__ = "reports"


# Defining primary key
    Report_id = Column(Integer, primary_key=True, index=True)


# Linking report to the Task it belongs to
    Task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)


# Adding task name field
    Task_name=Column(String(255),nullable=False)


#Adding project name field
    Project_name=Column(String(255),nullable=False)


#Adding user reporting field
    Reported_by_name=Column(String(255),nullable=False)


# Linking report to the User who submitted it
    User_id = Column(Integer, ForeignKey("user.id"), nullable=False)


# Adding Rate field
    Rate=Column(Float,nullable=False)


#Adding amount field    
    Amount=Column(Float,nullable=False)


#Adding Status field
    Status=Column(String(255),nullable=False)


#Adding Pending_Quantity field
    Pending_quantity=Column(String(255),nullable=False)        


# Adding timestamp field
    Timestamp= Column(DateTime, default=datetime.utcnow)


#Adding Overall Quantity field
    Overall_quantity=Column(Integer,nullable=False)


#Adding Reported Quantity field
    Reported_quantity=Column(Integer,nullable=False)  


# Creating relationship with Task model
    task = relationship("Task", back_populates="reports")


# Creating relationship with User model
    user = relationship("User", back_populates="reports")


#Inserting dummy report data
if __name__ == "__main__":


# Creating DB session
    db = SessionLocal()


# Fetching one user and one task to link with the report
    user = db.query(User).filter_by(email="emp1@example.com").first()
    task = db.query(Task).filter_by(name="Planning and Designing").first()


# Inserting dummy report only if task and user exist
    if user and task:
        report = Report(
            task_id=task.id,
            user_id=user.id,
            content="Completed initial UI wireframes and discussed backend flow with team."
        )
        db.add(report)
        db.commit()
        print(f"Report submitted by {user.email} for task '{task.name}'")
    else:
        print("User or Task not found. Please ensure dummy data exists first.")


# Closing session
    db.close()
