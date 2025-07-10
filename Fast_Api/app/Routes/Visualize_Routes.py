from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.Database import get_db
from app.models import Task, Report


# Creating a router for all visualization related endpoints
router = APIRouter()


#Task Progress Chart (Completed vs In Progress)
@router.get("/visualize/task-progress")
def get_task_progress_chart(db: Session = Depends(get_db)):
    result = db.query(
        Task.name.label("task_name"),
        func.count(func.nullif(Report.Status != "Completed", True)).label("completed_count"),
        func.count(func.nullif(Report.Status != "In Progress", True)).label("in_progress_count")
    ).join(Report, Task.id == Report.Task_id).group_by(Task.name).all()

    return {
        "data": [
            {
                "task_name": row.task_name,
                "completed_count": row.completed_count,
                "in_progress_count": row.in_progress_count
            }
            for row in result
        ]
    }

# Project-wise Task Count
@router.get("/visualize/project-task-counts")
def get_project_task_counts(db: Session = Depends(get_db)):
    result = db.query(
        Report.Project_name, 
        func.count(Task.id).label("task_count")
    ).join(Task, Task.id == Report.Task_id).group_by(Report.Project_name).all()

    return {
        "data": [
            {
                "project_name": row.Project_name,
                "task_count": row.task_count
            }
            for row in result
        ]
    }