from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Task, Base
from database import DB_URL

app = FastAPI()

# Database setup
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Pydantic schema
class TaskCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new task
@app.post("/tasks", response_model=dict)
def create_task(task: TaskCreate, db: SessionLocal = Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed": new_task.completed
    }

# Get all tasks
@app.get("/tasks", response_model=list[dict])
def get_tasks(db: SessionLocal = Depends(get_db)):
    tasks = db.query(Task).all()
    return [
        {"id": t.id, "title": t.title, "description": t.description, "completed": t.completed}
        for t in tasks
    ]

@app.get("/tasks/{task_id}", response_model=dict)
def get_task(task_id: int, db: SessionLocal = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    
# Update an existing task
@app.put("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, task: TaskUpdate, db: SessionLocal = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed
    }

# Delete a task
@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: SessionLocal = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
