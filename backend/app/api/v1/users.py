from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash
from app.api.v1.auth import require_admin

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), current_admin: User = Depends(require_admin)):
    """Apenas Administradores podem criar novos Colaboradores ou Admins"""
    db_user = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system."
        )
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db), current_admin: User = Depends(require_admin)):
    """Listar usuários (Admin)"""
    users = db.query(User).all()
    return users
