from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS — the bundled frontend (frontend/index.html) is served from a different origin
# (file:// or a separate static server) and would otherwise be blocked by the browser.
# Tighten allow_origins before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- DB session dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Schemas ---
# Split into three: clients posting a new task can't (and shouldn't) supply an id,
# and responses always include one.
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False


class TaskUpdate(TaskCreate):
    """Same shape as TaskCreate — clients PUT the full new state of the task."""


class TaskResponse(TaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Endpoints ---
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(title: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Task)
    if title:
        query = query.filter(models.Task.title.contains(title))
    return query.all()


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = updated.title
    db_task.description = updated.description
    db_task.is_completed = updated.is_completed

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} has been deleted"}
