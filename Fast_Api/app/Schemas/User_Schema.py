from pydantic import BaseModel,Field,EmailStr
from typing import Optional

# Schema for creating a role
class RoleSchema(BaseModel):
    name: str

# Schema used for creating a new user
class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    role: str
    user_name: str 

# Schema used during user signup
class SignUpSchema(BaseModel):
    email: EmailStr
    password: str
    role: str

# Schema used for user login
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

#Schema for user and task
class UserTaskInput(BaseModel):
    user_id: int
    task_id: int
    task_name: str
class Config:
    orm_mode = True
