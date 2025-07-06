from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate  

# Initializing database, JWT, and migration extension objects
db = SQLAlchemy()
jwt = JWTManager()

load_dotenv()
migrate = Migrate() 

def create_app():
    app = Flask(__name__)

    # Loading all configuration values from app/config.py file
    app.config.from_object('app.config.Config')

    # Just to make sure the DB connection string was loaded correctly
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Initialize Flask extensions (database and JWT handling)
    db.init_app(app)
    jwt.init_app(app)

    migrate.init_app(app, db) 
    # To avoid circular issues
    with app.app_context():
        from app.models.User import User
        from app.models.Role import Role
        from app.models.Projects import Project
        from app.models.Projects_User import ProjectUser
        from app.models.Task import Task  # Add this if Task model exists

     

    # Register authentication-related routes under /api/auth
    from app.Routes.Authentication_Routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Register project-related routes under /api/project
    from app.Routes.Project_Routes import project_bp
    app.register_blueprint(project_bp, url_prefix='/api/project')

    # Register user-related routes under /api/user
    from app.Routes.User_Routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/user')

    # Printing routes to confirm their existence
    with app.app_context():
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)

    print("auth_bp loaded")
    return app
