from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Load config from app/config.py 
    app.config.from_object('app.config.Config')

    # Debug print to verify DB URI loaded
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import models AFTER initializing db to avoid circular import issues
    with app.app_context():
        from app.models.User import User
        from app.models.Role import Role
        from app.models.Projects import Project
        from app.models.Projects_User import ProjectUser
    
        db.create_all()

    # Register blueprints
    from app.Routes.Authentication_Routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.Routes.Project_Routes import project_bp
    app.register_blueprint(project_bp, url_prefix='/api/project')

    print("auth_bp loaded")
    return app
