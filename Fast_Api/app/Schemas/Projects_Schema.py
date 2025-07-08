# Importing BaseModel from Pydantic for data validation and parsing
from pydantic import BaseModel

#Schema for creating projects
class CreateProjectSchema(BaseModel):
    name: str

#Schema for assigning projects to employees
class AssignProjectSchema(BaseModel):
    project_id: int
    user_id: int
