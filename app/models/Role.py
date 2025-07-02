from app import db

# Defining the Role model to store user roles in the system
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each role
    name = db.Column(db.String(50), unique=True, nullable=False)  # Role name (must be unique and not null)


# Defining a function to insert predefined roles into the database
def insert_roles():
    # List of default role names
    roles = [
        'CEO', 'Project Manager', 'Project Coordinator', 'Employee', 'Intern',
        'Team Lead', 'QA Engineer', 'Designer', 'HR Manager', 'Data Analyst'
    ]

    # Looping through each role
    for name in roles:
        # If role doesn't already exist, insert it
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))

    # Saving changes to the database
    db.session.commit()


if __name__ == "__main__":
   # Importing the app factory function
    from app import create_app
     # Creating Flask app instance
    app = create_app()        
    # Pushing application context for DB access
    app.app_context().push()  
    # Inserting roles
    insert_roles()
    print("Roles inserted successfully.")
