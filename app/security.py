from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id),
               "exp": datetime.now(UTC) + timedelta(hours=24)}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")