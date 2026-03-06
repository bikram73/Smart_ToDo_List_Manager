from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.auth_db import get_auth_db
from models.user_model import User, UserCreate, UserLogin
from utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_auth_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_auth_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # We store user_id in the token 'sub' claim to use it in Todo DB operations
    access_token = create_access_token(data={"sub": str(db_user.id), "username": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
