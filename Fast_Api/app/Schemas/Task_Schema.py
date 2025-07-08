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
    name: str
    start_date: date
    end_date: date
    project_id: int

# For returning task from API
class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True
