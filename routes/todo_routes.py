from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database.todo_db import get_todo_db
from models.todo_model import Todo, TodoCreate, TodoUpdate, TodoResponse
from utils.security import get_current_user_id
from datetime import date, datetime

router = APIRouter()

@router.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    new_todo = Todo(
        task=todo.task, 
        user_id=user_id, 
        status="pending",
        task_date=todo.task_date,
        start_time=todo.start_time,
        end_time=todo.end_time
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    todos = db.query(Todo).filter(Todo.user_id == user_id).all()
    return todos

@router.get("/todos/date/{date_str}", response_model=List[TodoResponse])
def get_todos_by_date(date_str: date, db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    todos = db.query(Todo).filter(Todo.user_id == user_id, Todo.task_date == date_str).all()
    return todos

@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.task:
        todo.task = todo_update.task
    if todo_update.status:
        todo.status = todo_update.status
    if todo_update.task_date:
        todo.task_date = todo_update.task_date
    if todo_update.start_time:
        todo.start_time = todo_update.start_time
    if todo_update.end_time:
        todo.end_time = todo_update.end_time
        
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}

@router.patch("/todos/{todo_id}/complete")
def mark_complete(todo_id: int, db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.status = "completed"
    db.commit()
    return {"message": "Todo marked as completed"}

@router.patch("/todos/{todo_id}/move-to-today")
def move_to_today(todo_id: int, db: Session = Depends(get_todo_db), user_id: int = Depends(get_current_user_id)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.task_date = datetime.now().date()
    db.commit()
    return {"message": "Todo moved to today"}
