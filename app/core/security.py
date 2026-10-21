from jose import jwt
from datetime import datetime, timedelta, timezone
from .config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from pwdlib import PasswordHash
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

password_hash = PasswordHash.recommended()

def generate_access_token(user_id: int):    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    return payload

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password
    )

def hash_password(password: str) -> str:
    return password_hash.hash(password)
