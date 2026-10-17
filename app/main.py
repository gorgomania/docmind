from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserRead
from app.security import hash_password

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
    


