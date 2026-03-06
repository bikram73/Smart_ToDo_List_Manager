from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.auth_db import get_auth_db
from models.user_model import User, UserUpdate
from utils.security import get_current_user_id, get_password_hash

router = APIRouter()

@router.get("/profile")
def get_profile(db: Session = Depends(get_auth_db), user_id: int = Depends(get_current_user_id)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "email": user.email
    }

@router.put("/profile")
def update_profile(user_update: UserUpdate, db: Session = Depends(get_auth_db), user_id: int = Depends(get_current_user_id)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username:
        # Check uniqueness
        existing = db.query(User).filter(User.username == user_update.username, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = user_update.username
        
    if user_update.email:
        user.email = user_update.email
        
    if user_update.password:
        user.password_hash = get_password_hash(user_update.password)
        
    db.commit()
    return {"message": "Profile updated successfully"}