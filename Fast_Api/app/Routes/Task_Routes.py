from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.Database import SessionLocal
from app.models.Task import Task as TaskModel
from app.Schemas.Task_Schema import TaskCreate, TaskOut,TaskUpdate
from typing import List

# Creating a router for all tasks related endpoints
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creating Task
@router.post("/tasks/", response_model=List[TaskOut])
async def create_tasks(tasks: List[TaskCreate], db: Session = Depends(get_db)):
    created_tasks = []
    for task in tasks:
        new_task = TaskModel(**task.dict())
        db.add(new_task)
        db.flush()  
        created_tasks.append(new_task)
    db.commit()
    return created_tasks

#Updating Task
@router.put("/update-task/{task_id}")
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task.Rate = data.Rate
    task.Quantity = data.Quantity

    db.commit()
    db.refresh(task)
    return {"message": "Task updated", "task_id": task.id}

#Getting All Tasks
@router.get("/", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

#Getting One Task by ID
@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#Updating Task
@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.name = updated_task.name
    task.description = updated_task.description
    db.commit()
    db.refresh(task)
    return task

#Deleting Task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
