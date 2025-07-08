from fastapi import APIRouter
from app.Routes.User_Routes import router as user_router
from app.Routes.Authentication_Routes import router as auth_router
from app.Routes.Project_Routes import router as project_router

# Creating a central API router
api_router = APIRouter()

# Including user-related routes
api_router.include_router(user_router, prefix="/user", tags=["User"])

# Including authentication-related routes
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Including project-related routes
api_router.include_router(project_router, prefix="/project", tags=["Project"])

# Exporting only the api_router
__all__ = ["api_router"]
