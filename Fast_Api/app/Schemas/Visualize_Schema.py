from pydantic import BaseModel

#Schema to check tasks progress
class TaskProgressOut(BaseModel):
    task_name: str
    completed_count: int
    in_progress_count: int

    class Config:
        orm_mode = True

#Schema to check Tasks count
class ProjectTaskCountOut(BaseModel):
    project_name: str
    task_count: int


# Enabling compatibility with ORM objects like SQLAlchemy models
# Allowing Pydantic to read data directly from model instances 
class Config:
    orm_mode = True