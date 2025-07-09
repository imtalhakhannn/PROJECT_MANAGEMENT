from fastapi import APIRouter, Request, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.Schemas.User_Schema import UserCreateSchema,SignUpSchema,LoginSchema
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.User import User
from app.models.Role import Role
from app.Database import get_db
from fastapi_jwt_auth import AuthJWT
import bcrypt
from app.authentication.utils import create_access_token
from app.Database import Base, SessionLocal
router = APIRouter()


#Creating Signup Api
@router.post("/signup")
async def signup(data: UserCreateSchema, db: Session = Depends(get_db)):
    # Checking if user already exists
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    # Checking if the provided role exists
    role = db.query(Role).filter_by(name=data.role).first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{data.role}' not found. Please create it first.")

    # Creating user with hashed password
    new_user = User(
        email=data.email,
        password=generate_password_hash(data.password),
        role_id=role.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id, "role": role.name}

#Creating login Api
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Finding user in the database by email
    user = db.query(User).filter(User.email == data.email).first()

    # If user not found or password does not match
    if not user or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generating JWT access token using user's ID (can also use email)
    access_token = Authorize.create_access_token(subject=str(user.id))

    # Returning token and some user info
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email,
        "role": user.role.name
    }

#CReating Role Api
@router.post("/create-role")
async def create_role(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")

    if not name:
        return JSONResponse(content={"msg": "Role name required"}, status_code=400)

    if db.query(Role).filter_by(name=name).first():
        return JSONResponse(content={"msg": "Role already exists"}, status_code=400)

    new_role = Role(name=name)
    db.add(new_role)
    db.commit()

    return JSONResponse(content={"msg": f"Role '{name}' created successfully"}, status_code=201)
