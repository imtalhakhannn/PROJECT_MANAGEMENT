from pydantic import BaseModel
from datetime import date

#Base class
class TaskBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    project_id: int

#For creating new task
class TaskCreate(TaskBase):
    pass
#Updating Tasks Table by adding Quantity and Rate columns
class TaskUpdate(TaskBase):
    Rate: str
    Quantity: int

# For returning task from API
class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True
