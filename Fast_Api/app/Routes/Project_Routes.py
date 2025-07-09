from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.Project import Project
from app.models.ProjectUser import ProjectUser
from app.models.Task import Task
from app.models.User import User
from app.Database import get_db
from app.authentication.utils import get_current_user_with_roles
from app.Schemas.Projects_Schema import CreateProjectSchema,AssignProjectSchema


# Creating a router for all projects related endpoints
router = APIRouter(prefix="/project", tags=["Projects"])


#Creating Project 
@router.post("/create")
async def create_project(
    data: CreateProjectSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_roles(["Project Manager"]))
):
    name = data.name.strip()

    if not name:
        return JSONResponse(status_code=400, content={"msg": "Project name must be a non-empty string"})

    project = Project(name=name.strip(), manager_id=current_user.id)
    db.add(project)
    db.commit()

    return JSONResponse(status_code=201, content={"msg": "Project created successfully", "project_id": project.id})


# Assigning User to Project 
@router.post("/assign")
async def assign_user(
    data: AssignProjectSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_roles(["Project Manager"]))
):
   
    project_id = data.project_id
    user_id = data.user_id

    project = db.query(Project).get(project_id)
    if not project:
        return JSONResponse(status_code=404, content={"msg": "Project not found"})

    if project.manager_id != current_user.id:
        return JSONResponse(status_code=403, content={"msg": "Unauthorized to assign users"})

    user = db.query(User).get(user_id)
    if not user:
        return JSONResponse(status_code=404, content={"msg": "User not found"})

    if db.query(ProjectUser).filter_by(project_id=project_id, user_id=user_id).first():
        return JSONResponse(status_code=400, content={"msg": "User already assigned"})

    assignment = ProjectUser(project_id=project_id, user_id=user_id)
    db.add(assignment)
    db.commit()

    return JSONResponse(content={"msg": "User assigned to project successfully"})


#Getting Projects Created by Logged in project manager
@router.get("/created")
def get_pm_created_projects(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    try:
        Authorize.jwt_required()


# Getting user ID from JWT
        user_id = Authorize.get_jwt_subject()

        current_user = db.query(User).filter(User.id == user_id).first()
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")

        created_projects = db.query(Project).filter(Project.manager_id == current_user.id).all()

# Converting projects to dict safely 
        project_list = [project.to_dict() if hasattr(project, "to_dict") else {
            "id": project.id,
            "name": project.name,
            "manager_id": project.manager_id
        } for project in created_projects]

        return {"projects": project_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching created projects: {str(e)}")
