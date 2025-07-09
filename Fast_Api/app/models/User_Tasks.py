from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.Database import Base


# Defining the UserTask table 
class UserTask(Base):
    __tablename__ = "user_tasks"


# Defining primary key for the user task
    id = Column(Integer, primary_key=True, index=True)
    

# Storing reference to the user who performed the task
    user_id = Column(Integer, ForeignKey("user.id"))
    

# Storing the associated task ID
    task_id = Column(Integer)
    

# Storing the name of the task
    task_name = Column("task_name", String(255))


# Establishing relationship with the User model
    user = relationship("User", back_populates="user_tasks")
