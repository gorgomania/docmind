from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserRead
from app.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Annotated[Session, Depends(get_db)]):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}

@app.post("/auth/register", response_model=UserRead, status_code=201)
def register(user_in: UserCreate, db: Annotated[Session, Depends(get_db)]):
    existing = db.scalar(select(User).where(User.email == user_in.email))

    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@app.post("/auth/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.email == form_data.username))
    
    if not (user and verify_password(form_data.password, user.hashed_password)):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me", response_model=UserRead)
def read_me(user: Annotated[User, Depends(get_current_user)]):
    return user