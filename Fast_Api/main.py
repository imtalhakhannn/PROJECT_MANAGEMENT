from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel


# JWT Secret Key Configuration
class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret"  

@AuthJWT.load_config
def get_config():
    return Settings()


# Initializing FastAPI App
app = FastAPI(title="Project Management API")


# Custom OpenAPI for Swagger Authorization
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Project Management API",
        version="1.0.0",
        description="API for task, user, project, and report management with JWT Auth",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Including API Routers
from app.Routes import Task_Routes, Project_Routes, User_Routes, Report_Routes,Visualize_Routes
from app.Routes.Authentication_Routes import router as auth_router  
app.include_router(auth_router)
app.include_router(Task_Routes.router)
app.include_router(Project_Routes.router)
app.include_router(User_Routes.router)
app.include_router(Report_Routes.router)
app.include_router(Visualize_Routes.router)
from app.Database import Base, engine  
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Project Management API is running"}