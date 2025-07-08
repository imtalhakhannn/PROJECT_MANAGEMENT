from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating a role
class RoleSchema(BaseModel):
    name: str

# Schema used for creating a new user
class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    role: str

# Schema used during user signup
class SignUpSchema(BaseModel):
    email: EmailStr
    password: str
    role: str

# Schema used for user login
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
