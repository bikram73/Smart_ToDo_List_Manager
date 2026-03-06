from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import auth_routes, todo_routes, user_routes
from database.auth_db import engine as auth_engine, Base as AuthBase
from database.todo_db import engine as todo_engine, Base as TodoBase, SessionLocal
from models.todo_model import Todo
from models.user_model import User
from services.email_service import send_email_reminder
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_

# Create Tables (For production, use Alembic migrations, but this works for MVP)
# Wrap in try-except to prevent Vercel "Function Invocation Failed" if DB connection fails or is read-only
try:
    AuthBase.metadata.create_all(bind=auth_engine)
    TodoBase.metadata.create_all(bind=todo_engine)
except Exception as e:
    print(f"Startup Error: Could not create tables. {e}")

app = FastAPI(title="Smart To-Do List Manager")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_routes.router, prefix="/api", tags=["Authentication"])
app.include_router(todo_routes.router, prefix="/api", tags=["Todos"])
app.include_router(user_routes.router, prefix="/api/user", tags=["User"])

@app.get("/api")
def root():
    return {"message": "Welcome to Smart To-Do List API"}

@app.get("/api/cron/reminders")
def check_reminders():
    """
    This endpoint is designed to be called by a Cron Job (e.g., Vercel Cron)
    every few minutes to check for overdue tasks and send emails.
    """
    db = SessionLocal()
    
    # Create Auth DB Session manually to fetch user emails
    AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)
    auth_db = AuthSessionLocal()

    try:
        now = datetime.now()
        current_time = now.time()
        current_date = now.date()

        # Find tasks that are:
        # 1. Pending
        # 2. Have a date of today (or past)
        # 3. Have an end_time that has passed
        # 4. Have not had an email sent yet
        
        overdue_todos = db.query(Todo).filter(
            Todo.status == "pending",
            Todo.end_time != None,
            Todo.email_sent == False,
            or_(
                Todo.task_date < current_date,
                and_(Todo.task_date == current_date, Todo.end_time < current_time)
            )
        ).all()

        sent_count = 0
        for todo in overdue_todos:
            # Fetch user from Auth DB
            user = auth_db.query(User).filter(User.id == todo.user_id).first()
            
            if user and user.email:
                try:
                    send_email_reminder(user.email, todo.task)
                    todo.email_sent = True
                    sent_count += 1
                except Exception as e:
                    print(f"Failed to send email to {user.email}: {e}")
        
        db.commit()
        return {"message": f"Checked tasks. Sent {sent_count} reminders."}
    finally:
        db.close()
        auth_db.close()

# Mount frontend static files (Place this after API routes so API takes precedence)
# Use absolute path for Vercel environment
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, "../frontend")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
elif os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
