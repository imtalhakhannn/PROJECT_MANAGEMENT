from app import db
from datetime import date
from sqlalchemy import Date
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True,nullable=False)
    start_date=db.Column(Date,nullable=False)
    end_date=db.Column(Date,nullable=False)
    #Using Foreign key from Project Table to link with Task Table
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

if __name__=="__main__":
    from app import app
    with app.app_context():
        db.create_all()
        task=Task(name="Planning and Designing",
                  start_date=date(2025,8,13),
                  end_date=date(2025,10,20),
                  project_id=1)

        db.session.add(task)
        db.session.commit()
        print(f"The task'{task.name}'is added")