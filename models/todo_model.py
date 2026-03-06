from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, Boolean
from database.todo_db import Base
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    task = Column(Text)
    status = Column(String(20), default="pending")
    task_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    email_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TodoCreate(BaseModel):
    task: str
    task_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class TodoUpdate(BaseModel):
    task: Optional[str] = None
    status: Optional[str] = None
    task_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class TodoResponse(BaseModel):
    id: int
    task: str
    status: str
    task_date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    created_at: datetime