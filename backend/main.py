from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Create the database tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Dependency ---
# This helper function opens a connection to the DB for a request,
# and closes it when the request is done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Models (Data Validation) ---
# We use this for input/output validation, separate from the Database Model
from pydantic import BaseModel, ConfigDict # Add ConfigDict to your imports

class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) # This is the modern way
    
    title: str
    description: Optional[str] = None
    is_completed: bool = False
# --- API Endpoints ---

@app.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    # Create a new instance of the Database Model
    new_task = models.Task(
        title=task.title, 
        description=task.description, 
        is_completed=task.is_completed
    )
    db.add(new_task)      # Add to session
    db.commit()           # Save to DB
    db.refresh(new_task)  # Refresh to get the new ID
    return new_task

# Update your GET tasks function to look like this:
@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks(title: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Task)
    
    # If the user provides a title, filter the results
    if title:
        query = query.filter(models.Task.title.contains(title))
    
    return query.all()

@app.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# UPDATE: Change a task's title or completion status
@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, updated_data: TaskSchema, db: Session = Depends(get_db)):
    # 1. Look for the task in the DB
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    # 2. If it doesn't exist, tell the user
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 3. Update the fields
    db_task.title = updated_data.title
    db_task.description = updated_data.description
    db_task.is_completed = updated_data.is_completed
    
    # 4. Save the changes
    db.commit()
    db.refresh(db_task)
    return db_task

# DELETE: Remove a task from the database
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} has been deleted"}