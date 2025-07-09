# Importing Pydantic schemas for report input/output
from app.Schemas.Report_Schema import ReportCreate, ReportOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Database import get_db
from app.models.Report import Report
from app.models.User import User
from app.models.Task import Task


# Creating a router for all reports related endpoints
router = APIRouter()


# Creating a new report and linking it with user and task
@router.post("/reports/", response_model=ReportOut)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):


# Fetching user and task to ensure they exist
    user = db.query(User).get(report.user_id)
    task = db.query(Task).get(report.task_id)


# Raising error if user or task doesn't exist
    if not user or not task:
        raise HTTPException(status_code=404, detail="User or Task not found")
    

# Creating and saving the new report
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)


# Returning the created report
    return db_report


# Fetching all reports from the database
@router.get("/reports/", response_model=list[ReportOut])
def get_all_reports(db: Session = Depends(get_db)):
    return db.query(Report).all()


# Fetching a single report by its ID
@router.get("/reports/{report_id}", response_model=ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):


# Retrieving the report by primary key
    report = db.query(Report).get(report_id)


# Raising error if not found
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report
