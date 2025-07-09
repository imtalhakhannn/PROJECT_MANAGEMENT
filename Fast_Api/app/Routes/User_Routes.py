from fastapi import Request, status
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.User import User
from app.models.Role import Role
from app.models.Task import Task
from app.Database import get_db
from app.authentication.utils import get_current_user_with_roles
from werkzeug.security import generate_password_hash
from app.Schemas.User_Schema import UserCreateSchema,RoleSchema,UserTaskInput
from app.models.User_Tasks import UserTask

router = APIRouter()
#Creating role for a specific user
@router.post("/create-role")
async def create_role(data: RoleSchema, db: Session = Depends(get_db)):
    if db.query(Role).filter_by(name=data.name).first():
        return JSONResponse(content={"msg": "Role already exists"}, status_code=400)

    new_role = Role(name=data.name)
    db.add(new_role)
    db.commit()

    return JSONResponse(content={"msg": f"Role '{data.name}' created successfully"}, status_code=201)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User

from app.authentication.utils import get_current_user
import bcrypt

router = APIRouter()
#Creating Users according to the position
@router.post("/create-user")
def create_user(
    data: UserCreateSchema = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #If user is CEO then it can hire project manager,hr manager and employee
    if current_user.role.name == "CEO":
        if data.role not in ["HR Manager", "Project Manager","Employee"]:
            raise HTTPException(status_code=400, detail="CEO can only create HR,Project Manager and Employees.")
    #if user is project manager and HR Manager they can both hire employees    
    elif current_user.role.name in ["HR Manager", "Project Manager"]:
        if data.role != "Employee":
            raise HTTPException(status_code=400, detail="You can only create Employee accounts.")
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to create users.")

    existing_user = db.query(User).filter_by(email=data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    role_obj = db.query(Role).filter_by(name=data.role).first()
    if not role_obj:
        raise HTTPException(status_code=400, detail="Invalid role.")

    hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    new_user = User(email=data.email, password=hashed_password, role=role_obj)
    new_user = User(
        email=data.email,
        password=hashed_password,
        role=role_obj,
        created_by=current_user.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"{data.role} created successfully", "email": new_user.email}

#Getting all users created by CEO,project manager and HR Manager
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_roles(["CEO", "Project Manager", "HR Manager"]))
):
    # CEO can see all users
    if current_user.role.name == "CEO":
        return db.query(User).all()
    
    # Others see only the users they created
    users = db.query(User).filter(User.created_by == current_user.id).all()
    return users

#Updating for users and tasks
@router.post("/add")
def add_user_task(data: UserTaskInput, db: Session = Depends(get_db)):
    try:
        # Getting task name using task_id
        task = db.query(Task).filter(Task.id == data.task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Inserting into user_tasks
        new_entry = UserTask(user_id=data.user_id, task_id=data.task_id,task_name=task.name)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return {
            "message": "Task assigned to user successfully",
            "user_task": {
                "id": new_entry.id,
                "user_id": new_entry.user_id,
                "task_id": new_entry.task_id,
                "task_name": task.name  
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))