# Defining the configuration class for the Flask application
class Config:
    # Setting the database URI using MySQL with pymysql driver
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pakistan%40321%24@localhost/project_manager'
    
    # Disabling SQLAlchemy event system to save resources 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Defining the secret key used for signing JWT tokens 
    JWT_SECRET_KEY = 'your-secret-key'  